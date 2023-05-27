import speech_recognition as sr
import pyttsx3
import requests
import json
from datetime import datetime

# Set up the speech recognition object
r = sr.Recognizer()

# Set up the text-to-speech object
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# ChatGPT API details
API_KEY = 'your api'
API_URL = 'https://api.openai.com/v1/chat/completions'

# Function to send a message to ChatGPT API and get a response
def get_chatbot_response(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': message}],
        'model': 'gpt-3.5-turbo'  # Specify the model here
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response_data = json.loads(response.text)
    
    # Debugging: Print the response data
    # print(response_data)
    
    if 'choices' in response_data and len(response_data['choices']) > 0:
        return response_data['choices'][0]['message']['content']
    else:
        return "Sorry, I couldn't generate a response."

# Function to convert text to speech and read it aloud
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user based on the current time
def greet_user():
    current_time = datetime.now().time()
    if current_time.hour < 12:
        greeting = 'Good morning!'
    elif current_time.hour < 18:
        greeting = 'Good afternoon'
        print("Bot:", greeting)
    speak(greeting)

# Main program loop
greet_user()

while True:
    # Listen to the user's voice input
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        # Recognize speech using Google Speech Recognition
        user_input = r.recognize_google(audio)
        print("User:", user_input)

        # Get response from ChatGPT
        response = get_chatbot_response(user_input)
        print("Bot:", response)

        # Speak the response
        speak(response)

    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")

    except sr.RequestError as e:
        print("Sorry, I'm currently unavailable. Please try again later.")

    except Exception as e:
        print("Sorry, an error occurred:", str(e))
