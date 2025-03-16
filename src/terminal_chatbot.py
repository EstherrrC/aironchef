import requests
import sys
import threading
import time
import yaml
import onnxruntime as ort
import numpy as np
import cv2
import os

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
        self.onnx_model_path = "efficientnet_b4.onnx"
        self.session = ort.InferenceSession(self.onnx_model_path)

        # Load class labels
        self.classes = []
        with open("cv/imagenet_class.txt", "r") as file:
            for line in file:
                self.classes.append(line.strip())

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

        # Check if the user wants to generate a recipe
        if message.lower().startswith("generate recipe"):
            ingredients = self.read_ingredients()
            stop_loading = True
            loading_thread.join()
            if "not found" in ingredients.lower():
                return "I couldn't find any ingredients in your fridge. Please update the file."

        system_prompt = (
        "You are an AI-powered nutritionist and meal planner. Your task is to generate a personalized daily meal plan (breakfast, lunch, and dinner) based on the user's health goals, dietary restrictions, and available ingredients. User Profile Information: Name: James Miller, Age: 30, Gender: Male. User Health Goals & Metrics: Health Goals (Multiple Selections): Muscle Gain, Heart Health. Current & Target Health Metrics: Weight: 75 kg → 80 kg, Body Fat Percentage: 18% → 15%, Muscle Mass: 30 kg → 35 kg, Blood Sugar Level: 5.8 mmol/L → 5.2 mmol/L, Cholesterol (LDL/HDL): LDL: 4.2 mmol/L (high) → LDL: 3.0 mmol/L (goal), Blood Pressure: 135/85 mmHg → 120/80 mmHg. Lifestyle Information: Exercise Routine: 4-5x per week (Strength Training & Cardio), Sleep Hours per Night: 7 hours, Other Lifestyle Factors: Occasional alcohol, no smoking, moderate stress. Target Timeline for Health Goals: 3 months. Dietary Preferences & Restrictions: Preferred Cuisines (Include Only Selected Options in Recipes): Western, Mediterranean. Food Restrictions (Strictly Avoided in Meal Plan): No Red Meat. Available Ingredients (STRICT – Use Only These)Use only the following ingredients in the meal plan. Do NOT include any other ingredients. Vegetables & Fruits: Cabbage, zucchini, mushroom, lemon, apple, banana. Grains & Breads: Dough, French loaf, bagel. Protein Sources: Meat loaf. Miscellaneous: Chocolate sauce, espresso, red wine. Structured Meal Plan Output Format: Generate a three-meal plan (breakfast, lunch, and dinner) based on the user's health goals and dietary preferences. Each meal should include: Meal Name, List of Ingredients Used, Step-by-Step Cooking Instructions, A brief explanation of why this meal supports the user's health goals."
        )

        return self.ask_chatbot(system_prompt)

        if not any(msg["role"] == "system" for msg in self.message_history):
            self.message_history.insert(0, {"role": "system", "content": system_prompt})

        short_term_memory = self.message_history[:1] + self.message_history[-19:]

        self.message_history.append({"role": "system", "content": system_prompt})
        self.message_history.append({"role": "user", "content": message})


        # Check if the user wants to classify an image
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

        chat_response = requests.post(self.chat_url, headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }, json=data)


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
    
    def preprocess_image(self, image_path) -> np.ndarray:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img

    def classify_image(self, image_path: str) -> str:
        input_name = self.session.get_inputs()[0].name
        input_tensor = self.preprocess_image(image_path)

        output = self.session.run(None, {input_name: input_tensor})

        class_idx = np.argmax(output[0])
        class_label = self.classes[class_idx]

        return f"Predicted class for image '{image_path}': {class_label}"

    def read_ingredients(self) -> str:
        try:
            with open("fridge_ingredient.txt", "r") as file:
                ingredients = file.read().strip()
            return ingredients
        except FileNotFoundError:
            return "Ingredients file not found."

    def ask_chatbot(self, prompt: str) -> str:
        """
        Send a custom message to the chatbot and return the response.
        """
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        data = {
            "message": prompt,
            "mode": "chat",
            "sessionId": "example-session-id",
            "attachments": [],
            "history": []
        }

        chat_response = requests.post(self.chat_url, headers=headers, json=data)

        try:
            return chat_response.json().get('textResponse', "I couldn't generate a recipe at the moment.")
        except ValueError:
            return "Response is not valid JSON"
        except Exception as e:
            return f"Chat request failed. Error: {e}"

# if __name__ == '__main__':
#     stop_loading = False
#     chatbot = Chatbot()
#     chatbot.run()