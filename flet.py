import flet as ft
import requests
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import openai
import json
import datetime
# Connect to MongoDB

uri = "https://ap-south-1.aws.data.mongodb-api.com/app/data-abcxa/endpoint/data/v1/action/insertOne"


def upload_to_db(id_date, key, value):
    payload = json.dumps({
        "collection": "BBOT",
        "database": "Techboys",
        "dataSource": "Cluster0",
        "document": {
            "_id": id_date,
            "key": key,
            "value": value
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'sC6c0nsPlmQuKYQOMrFmm2YCF52kFIUVKTC0J3Hzim6dXGeREuX9Kb0a6MectYed',
    }

    requests.request("POST", uri, headers=headers, data=payload)


def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Connect to OpenAI
load_dotenv()
OPENAI_KEY = os.getenv('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')

openai.api_key = OPENAI_KEY


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
        api_key="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",
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    message += str(response.choices[0].message)
    return message


messages = []

while (1):
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = getResponse(messages)
    upload_to_db(str(datetime.datetime.now()).strip(), "User", messages[-1])
    upload_to_db(str(datetime.datetime.now()).strip(), "BBOT", response)

    SpeakText(response)

    print(response)


def main(page: ft.Page):
    page.title = "BBOT"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER




ft.main()
