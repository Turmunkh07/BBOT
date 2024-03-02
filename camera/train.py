import datetime

import keyboard
import os
import time
from random import randint

import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def train_model():
    image_size = (150, 150)
    batch_size = 32

    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(image_size[0], image_size[1], 3)))
    model.add(MaxPooling2D(2, 2))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(2, 2))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(2, 2))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    train_datagen = ImageDataGenerator(rescale=1. / 255,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True)

    train_generator = train_datagen.flow_from_directory('./known/',
                                                        target_size=image_size,
                                                        batch_size=batch_size,
                                                        class_mode='binary')

    model.fit(train_generator, epochs=10)
    model.save('facial_recognition_model.h5')


def record_video(output_folder, duration=5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = os.path.join(output_folder, f"rec.avi")

    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))
    print(video_filename)

    recording = False

    print("Press 'R' to start/stop recording. Press 'Q' to quit.")

    start_time = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Video Recording", frame)

        key = cv2.waitKey(1)

        if keyboard.is_pressed('r'):
            if not recording:
                recording = True
                print("Recording started.")
                start_time = time.time()
            if time.time() - start_time >= duration:
                recording = False
                print("Recording stopped.")
                break

        if key & 0xFF == ord('q'):
            break

        if recording:
            out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def video_to_images(video_path, output_folder, frame_rate=30):
    cap = cv2.VideoCapture(video_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_rate = int(fps) if frame_rate > int(fps) else frame_rate

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % frame_rate == 0:
            image_filename = os.path.join(output_folder,
                                          f"{randint(1, 10) * randint(1, 10)}image-{frame_count:04d}.jpg")
            cv2.imwrite(image_filename, frame)

        frame_count += 1

    cap.release()


if __name__ == "__main__":
    record_video("./known/negative", 10)

    video_path = "./known/negative/rec.avi"

    output_folder = "./known/positive/rec.avi"

    frame_rate = 30

    video_to_images(video_path, output_folder, frame_rate)
