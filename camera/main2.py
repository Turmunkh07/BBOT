import cv2
import time
from deepface import DeepFace

# Load pre-trained emotion detection model
model = DeepFace.build_model("Emotion")

# Define emotion labels
emotion_labels = ['Surprise', 'Happy', 'Sad']  # Adjusted order

# Load Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load images for each emotion
emotion_images = {
    'Surprise': cv2.imread('/Users/anudarimunkhbat/Dcon turshilt/surprise/surprise.png'),
    'Happy': cv2.imread('/Users/anudarimunkhbat/Dcon turshilt/happy/happy.png'),
    'Sad': cv2.imread('/Users/anudarimunkhbat/Dcon turshilt/sad/sad.png')
}

# Function to detect faces and their emotions in the frame
def detect_faces_and_emotions(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50))
    for (x, y, w, h) in faces:
        face_roi = gray_frame[y:y + h, x:x + w]
        resized_face = cv2.resize(face_roi, (48, 48), interpolation=cv2.INTER_AREA)
        normalized_face = resized_face / 255.0
        reshaped_face = normalized_face.reshape(1, 48, 48, 1)
        preds = model.predict(reshaped_face)[0]
        emotion_idx = preds.argmax()
        if emotion_idx in [0, 1, 2]:  # Check for Surprise, Happy, Sad
            emotion = emotion_labels[emotion_idx]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            # Display the image corresponding to the recognized emotion
            if emotion in emotion_images:
                cv2.imshow(emotion, emotion_images[emotion])  # Display on a window named with emotion label
               # if emotion != 'Sad':  # Add delay when an emotion is recognized (except for Happy)
                    #time.sleep(2)  # 3 seconds delay
    return frame


# Main function to capture video from camera and perform emotion detection
def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Detect faces and emotions in the frame
        frame_with_emotions = detect_faces_and_emotions(frame)
        # Display the frame with emotion detection
        cv2.imshow('Real-time Emotion Detection', frame_with_emotions)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()