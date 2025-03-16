from src.gradio_chatbot import Chatbot

def main():
    print("Hi! How can I help you today?")

    history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        history.append({"role": "user", "content": user_input})

        if "upload" in user_input:
            response = {"role": "assistant", "content": "Collected! Do you want some recipe recommendation?"}
        else:
            response = {"role": "assistant", "content": chatbot.chat(user_input)}

        history.append(response)

        print(f"Chatbot: {response['content']}")

if __name__ == "__main__":
    main()