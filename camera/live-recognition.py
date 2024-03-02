import subprocess
import time

import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('./facial_recognition_model.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:

        face_roi = frame[y:y + h, x:x + w]

        face_roi = cv2.resize(face_roi, (150, 150))

        face_roi = np.expand_dims(face_roi, axis=0) / 255.0

        prediction = model.predict(face_roi)

        if prediction[0][0] > 0.80:
            cv2.putText(frame, "Owner", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print("Owner detected")
            exit()
        else:
            cv2.putText(frame, "Unknown Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow('Facial Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
