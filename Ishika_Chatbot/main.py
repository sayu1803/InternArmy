import nltk
import random
import requests
from bs4 import BeautifulSoup
from nltk.chat.util import Chat, reflections

# Predefined responses for the chatbot
responses = {
    "ishika": ["Yes, How can i help you today?"],
    "what is your name": ["My name is Ishika ChatBot. ❤️", "You can call me Ishika. ❤️"],
    "how are you": ["I'm doing well, thank you! 🥰", "I'm good, thanks for asking. 🥰"],
    "hello": ["Hi there! Ishika this side how can i assist you", "Hello!,Ishika here can i assist you", "Hey!, i'm Ishika how can i help you"],
    "hi": ["Hi there! Ishika this side how can i assist you", "Hello!,Ishika here can i assist you", "Hey!, i'm Ishika how can i help you"],
    "bye": ["Goodbye!", "Bye! Have a great day!"],
    "thanks": ["You're welcome!", "Glad I could help!", "My pleasure!"],
    "default": ["I'm not sure I understand.", "Can you please rephrase that?", "Sorry, I didn't get that."]
}

ishika_responses = {
    "ishika_info": ["Ishika is a friendly and helpful chatbot designed to assist users with various queries.", "Ishika is constantly learning and improving to provide better assistance to users."],
    "ishika_interaction": ["I'm here, how can I assist you?", "Yes, I'm Ishika! What do you need?", "Hello! How can I help you today?"],
    "ishika_fun_fact": ["Did you know? Ishika is named after the Sanskrit word meaning 'sacred' or 'divine'.", "Fun fact: Ishika loves learning new things and enjoys interacting with users!"],
    "ishika_capabilities": ["Ishika can assist you with a wide range of tasks including answering questions, providing information, and engaging in conversation.", "Ishika is equipped to handle various queries and provide helpful responses to users."],
    "ishika_casual_conversation": ["Let's chat! What's on your mind?", "I'm up for some casual conversation. What would you like to talk about?", "Sure, let's have a friendly chat!"]
}

rude_words = ["stupid", "idiot", "dumb", "ugly", "hate", "suck", "annoying","fuck"]
rude_behavior_count = 0

def detect_rude_behavior(user_input):
    for word in rude_words:
        if word in user_input.lower():
            return True
    return False

def handle_rude_behavior():
    global rude_behavior_count
    rude_behavior_count += 1
    if rude_behavior_count == 3:
        print("Ishika: You've behaved rudely more than twice. I'm ending our conversation. Goodbye!")
        exit()
    else:
        return random.choice(["Let's keep the conversation respectful.", "I'm here to help. Please refrain from using offensive language.", "Kindly maintain a polite tone in our conversation."])
def personalize_response(response, user_name=None):
    if "{name}" in response:
        if user_name:
            response = response.replace("{name}", user_name)
        else:
            response = response.replace("{name}", "")
    return response
def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='BNeawe')
    if results:
        search_results = [result.text for result in results]
        return search_results
    else:
        return ["Sorry, I couldn't find any relevant information. Here's a link for your query:", search_url]
def print_output(prefix, text):
    max_width = 80
    output_text = ' '.join(text)
    output_lines = [output_text[i:i+max_width] for i in range(0, len(output_text), max_width)]
    output_paragraph = ' '.join(output_lines)
    print(f"{prefix}: {output_paragraph}")

def chatbot():
    print("Welcome to Ishika ChatBot, you can call me Ishika ❤️")
    print("To know about me type:'ishika_interaction','ishika_info','ishika_fun_fact','ishika_capabilities','ishika_casual_conversation' ")
    print("Type 'bye' to exit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'bye':
            print("Ishika:",random.choice(responses["bye"]))
            break
        elif detect_rude_behavior(user_input):
            print("Ishika:", handle_rude_behavior())
        elif user_input.lower() in responses.keys():
            print("Ishika:", random.choice(responses[user_input.lower()]))
        elif user_input.lower() in ishika_responses.keys():
            print_output("Ishika:", random.choice(ishika_responses[user_input.lower()]))
        else:
            response = google_search(user_input)
            print_output("Ishika", [line for line in response])

if __name__ == "__main__":
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    chatbot()
