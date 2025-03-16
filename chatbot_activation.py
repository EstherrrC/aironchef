def handle_message(message):
    # Check if the keyword "Aironchef" is in the message
    if "Aironchef" in message:
        # Activate the chatbot
        return activate_chatbot()
    else:
        # Ignore or handle other messages
        return "I'm here if you need me!"


def activate_chatbot():
    # Logic to perform when the chatbot is activated
    return "Hello! I'm Aironchef. How can I assist you with your cooking today?"


# Example usage
user_message = "Can you help me, Aironchef?"
response = handle_message(user_message)
print(response) 