import sys
import os

# 设置项目的基础目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from terminal_chatbot import Chatbot

def main():
    print("Hi! How can I help you today?")

    chatbot = Chatbot()
    chatbot.run()

if __name__ == "__main__":
    main()