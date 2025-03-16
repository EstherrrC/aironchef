import gradio as gr
import requests
import yaml

class Chatbot:
    def __init__(self):
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)

        self.api_key = config["api_key"]
        self.base_url = config["model_server_base_url"]
        self.workspace_slug = config["workspace_slug"]

        self.chat_url = f"{self.base_url}/workspace/{self.workspace_slug}/chat"

    def chat(self, message: str) -> str:
        """
        Send a chat request to the model server and return the response

        Inputs:
        - message: The message to send to the chatbot
        """
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        data = {
            "message": message,
            "mode": "chat",
            "sessionId": "example-session-id",
            "attachments": []
        }

        chat_response = requests.post(
            self.chat_url,
            headers=headers,
            json=data
        )

        try:
            text_response = chat_response.json()['textResponse']
            return text_response
        except ValueError:
            return "Response is not valid JSON"
        except Exception as e:
            return f"Chat request failed. Error: {e}"

def main():
    chatbot = Chatbot()

    with gr.Blocks() as app:
        gr.Markdown("# Chatbot Interface")

        chatbot_widget = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.Button("Clear")

        def user_message(message, history):
            history.append([message, None])
            return "", history

        def bot_response(history):
            user_msg = history[-1][0]
            response = chatbot.chat(user_msg)
            history[-1][1] = response
            return history

        msg.submit(user_message, [msg, chatbot_widget], [msg, chatbot_widget], queue=False).then(
            bot_response, chatbot_widget, chatbot_widget
        )
        clear.click(lambda: None, None, chatbot_widget, queue=False)

    app.launch()

if __name__ == "__main__":
    main()