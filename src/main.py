from terminal_chatbot import Chatbot
from image_classifier import ImageClassifier
"""
he entry point of the application and will orchestrate interactions between 
the voice input, chatbot, and image classifier.
"""
def process_command(user_input, chatbot, classifier):
    if user_input.startswith("classify images"):
        image_paths = user_input.split()[2:]
        results = classifier.classify_images(image_paths)

        # Extract classified labels from results
        classified_labels = [line.split(": ")[1] for line in results.split("\n") if "File not found" not in line]

        if not classified_labels:
            return "No valid images classified."
        
        # Generate a recipe based on classified ingredients
        #recipe = chatbot.generate_recipe(classified_labels)
        return f"Classified ingredients: {', '.join(classified_labels)}\n"

        #return "\n".join([f"{img}: {label}" for img, label in results])
        #return classifier.classify_images(image_paths)
    else:
        return chatbot.chat(user_input)

if __name__ == "__main__":
    chatbot = Chatbot()
    classifier = ImageClassifier()

    while True:
        user_message = input("\nYou: ")
        if user_message.lower() in ["exit", "quit"]:
            break
        print("Agent:", process_command(user_message, chatbot, classifier))