from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1.types import RecognitionConfig, RecognitionAudio

import io
from google.oauth2 import service_account

# Load credentials from service account key file
credentials = service_account.Credentials.from_service_account_file(
    'stable-equator-412314-749eb84e41a1.json'
)

# Create a Speech Client using the provided credentials
client = speech.SpeechClient(credentials=credentials)

file_name = 'message-from-user.wav'
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()

# Configure the audio input
audio = RecognitionAudio(content=content)
config = RecognitionConfig(
    encoding=RecognitionConfig.AudioEncoding.LINEAR16,
    language_code='ja-JP',  # Language code for Japanese
)

# Perform the transcription
response = client.recognize(config=config, audio=audio)

# Print the transcription results
for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))
