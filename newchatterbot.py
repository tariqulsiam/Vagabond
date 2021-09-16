#! /usr/bin/python3
from chatterbot import ChatBot
chatbot = ChatBot("Vagabond")
from chatterbot.trainers import ListTrainer

conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]

trainer = ListTrainer(chatbot)

trainer.train()
while True:
    response = chatbot.get_response(input("Enter test: "))
    print(response)