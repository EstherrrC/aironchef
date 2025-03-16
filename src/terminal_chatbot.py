import requests
import sys
import threading
import time
import yaml

def loading_indicator() -> None:
    """
    Display a loading indicator in the console while the chat request is being processed
    """
    while not stop_loading:
        for _ in range(10):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write('\r' + ' ' * 10 + '\r')
        sys.stdout.flush()
    print('')

class Chatbot:
    def __init__(self):
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)

        self.api_key = config["api_key"]
        self.base_url = config["model_server_base_url"]
        self.workspace_slug = config["workspace_slug"]

        self.chat_url = f"{self.base_url}/workspace/{self.workspace_slug}/chat"

        self.message_history = []

    def run(self) -> None:
        """
        Run the chat application loop. The user can type messages to chat with the assistant.
        """
        while True:
            user_message = input("You: ")
            if user_message.lower() in ["exit", "quit"]:
                break
            try:
                print("Agent: " + self.chat(user_message))
            except Exception as e:
                print("Error! Check the model is correctly loaded. More details in README troubleshooting section.")
                sys.exit(f"Error details: {e}")
                

    def chat(self, message: str) -> str:
        """
        Send a chat request to the model server and return the response
        
        Inputs:
        - message: The message to send to the chatbot
        """
        global stop_loading
        stop_loading = False
        loading_thread = threading.Thread(target=loading_indicator)
        loading_thread.start()

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        self.message_history.append({
            "role": "user",
            "content": message
        })

        # create a short term memory bank with the last 20 messages
        short_term_memory = self.message_history[-20:]

        data = {
            "message": message,
            "mode": "chat",
            "sessionId": "example-session-id",
            "attachments": [],
            "history": short_term_memory
        }

        chat_response = requests.post(
            self.chat_url,
            headers=headers,
            json=data
        )

        stop_loading = True
        loading_thread.join()

        try:
            text_response = chat_response.json()['textResponse']
            self.message_history.append({
                "role": "assistant",
                "content": text_response
            })
            return text_response
        except ValueError:
            return "Response is not valid JSON"
        except Exception as e:
            return f"Chat request failed. Error: {e}"

if __name__ == '__main__':
    stop_loading = False
    chatbot = Chatbot()
    chatbot.run()