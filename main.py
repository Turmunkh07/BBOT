import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import openai
from pymongo import MongoClient

load_dotenv()
OPENAI_KEY = os.getenv('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')

openai.api_key = OPENAI_KEY

uri = "mongodb+srv://bbot-db:EVTEI4amitan@cluster0.bfoknxi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


# Initialize the recognizer
r = sr.Recognizer()


def record_text():
    while (1):
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = r.recognize_google(audio2)

                return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("I couldn't hear anything")


def getResponse(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    message.append(response.choices[0].message)
    return message


messages = []

while (1):
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = getResponse(messages)
    SpeakText(response)

    print(response)
