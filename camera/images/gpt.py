import cv2
from deepface import DeepFace

# Function to detect emotions in a frame
def detect_emotion(frame):
    # Analyze the emotion in the frame
    result = DeepFace.analyze(frame, actions=['emotion'])

    # Get the emotion with the highest probability
    emotion = max(result['emotion'], key=result['emotion'].get)

    return emotion

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Resize the frame to improve performance
    frame = cv2.resize(frame, (640, 480))

    # Detect emotion in the frame
    emotion = detect_emotion(frame)

    # Display the emotion on the frame
    cv2.putText(frame, emotion, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Emotion Detection', frame)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
