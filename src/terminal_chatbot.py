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

        # Load ONNX model
        #self.onnx_model_path = "efficientnet_b4.onnx"
        #self.session = ort.InferenceSession(self.onnx_model_path)

        # Load class labels
        #self.classes = []
        #with open("imagenet_class.txt", "r") as file:
            #for line in file:
                #self.classes.append(line.strip())

    
    def run(self) -> None:
        """
        Run the chat application loop. The user can type messages to chat with the assistant.
        """
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
        """
                

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

        # Check if the user wants to classify an image
        """
        if message.lower().startswith("classify image "):
            image_path = message.replace("classify image ", "").strip()
            if os.path.exists(image_path):
                stop_loading = True
                loading_thread.join()
                return self.classify_image(image_path)
            else:
                stop_loading = True
                loading_thread.join()
                return "Image file not found."
                """

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
            #"attachments": [],
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
    """
    def preprocess_image(self, image_path) -> np.ndarray:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img

    def classify_image(self, image_path: str) -> str:
        results = []
        input_name = self.session.get_inputs()[0].name

        for image_path in image_paths:
            input_tensor = self.preprocess_image(image_path)
            output = self.session.run(None, {input_name: input_tensor})

            class_idx = np.argmax(output[0])
            class_label = self.classes[class_idx]
            results.append((image_path, class_label))
            print(f"Image: {image_path} | Predicted class: {class_label}")

        return results
    
    def process_command(user_input):
        if user_input.startswith("classify images"):
            image_paths = user_input.split()[2:]  # Example: classify images image1.jpg image2.jpg
            results = classify_images(image_paths)
            return "\n".join([f"{img}: {label}" for img, label in results])
        else:
            return chatbot.chat(user_input)

    while True:
        user_message = input("You: ")
        print("Agent:", process_command(user_message))


if __name__ == '__main__':
    stop_loading = False
    chatbot = Chatbot()
    chatbot.run()
    """