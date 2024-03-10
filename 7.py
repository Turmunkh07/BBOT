import cv2
import time
from deepface import DeepFace


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
def get_emotion_from_webcam(duration, arr):
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


# Example usage:
emotions = []
duration = 3  # Duration in seconds
get_emotion_from_webcam(duration, arr=emotions)
for e in range(len(emotions)):
    if emotions.__contains__("No face detected"):
        emotions.remove("No face detected")
    if emotions.__contains__("Unknown"):
        emotions.remove("Unknown")

print(emotions[-1])