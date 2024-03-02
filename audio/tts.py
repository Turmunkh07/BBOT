from gtts import gTTS
import os

def text_to_speech(text, language='ja', filename='output.mp3'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)
    print("Model initialized")
    # Save the speech as an MP3 file
    tts.save(filename)
    print("File saved")
    # Play the speech using the default audio player on your system
    os.system(f'start {filename}')

text_to_speech("心配しないで、僕があなたの友達になるよ。")
