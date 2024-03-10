import sys
import datetime
import json
import os
import time

import cv2
import openai
import pyttsx3
import requests
from PySide6.QtWidgets import QApplication, QMainWindow
from deepface import DeepFace
from dotenv import load_dotenv
import speech_recognition as sr

from ui_mainwindow import Ui_MainWindow


def bbot():

    def record_text():
        while (1):
            try:
                # use the microphone as source for input.
                with sr.Microphone() as source2:
                    r.adjust_for_ambient_noise(source2, duration=0.5)

                    # listens for the user's input
                    audio2 = r.listen(source2)

                    # Using google to recognize audio
                    MyText = r.recognize_google(audio2)
                    print(MyText)
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
        return message

    def SpeakText(command):
        # Initialize the engine
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def detect_faces_and_emotions(frame):
        model = DeepFace.build_model("Emotion")
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        emotion_labels = {3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50))
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_roi = gray_frame[y:y + h, x:x + w]
            resized_face = cv2.resize(face_roi, (48, 48), interpolation=cv2.INTER_AREA)
            normalized_face = resized_face / 255.0
            reshaped_face = normalized_face.reshape(1, 48, 48, 1)
            preds = model.predict(reshaped_face)[0]
            emotion_idx = preds.argmax()
            emotion_label = emotion_labels.get(emotion_idx, "Unknown")
            return emotion_label
        else:
            return "No face detected"

    # Example usage:
    def getEmotion(duration, arr):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to open webcam.")
            return
        start_time = time.time()
        while (time.time() - start_time) < duration:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture frame.")
                break
            emotion = detect_faces_and_emotions(frame)
            print("Emotion detected:", emotion)  # Print the detected emotion in real-time
            arr.append(emotion)
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release the video capture object and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

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

    uri = "https://ap-south-1.aws.data.mongodb-api.com/app/data-abcxa/endpoint/data/v1/action/insertOne"

    # Connect to OpenAI
    load_dotenv()
    OPENAI_KEY = os.getenv('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')

    openai.api_key = OPENAI_KEY

    # Initialize the recognizer
    r = sr.Recognizer()

    messages = []
    messages.append({"role": "system", "content": "You are friends with the user."})
    getResponse(messages)

    emotions = []

    SpeakText("Hello, I'm listening")

    while (1):
        text = record_text()
        getEmotion(3, emotions)

        for i in range(len(emotions)):
            if emotions.__contains__("No face detected"):
                emotions.remove("No face detected")
            if emotions.__contains__("Unknown"):
                emotions.remove("Unknown")

        if not len(emotions):
            emotions.append("unknown")

        messages.append({"role": "user", "content": text + "The user is feeling " + emotions[-1]})
        response = getResponse(messages)
        upload_to_db(str(datetime.datetime.now()).strip(), "User", messages[-1])
        upload_to_db(str(datetime.datetime.now()).strip(), "BBOT", response)

        SpeakText(response)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app

        self.actionQuit.triggered.connect(self.quit)

    def quit(self):
        bbot()


app = QApplication(sys.argv)
w = MainWindow(app)
w.show()
app.exec()
