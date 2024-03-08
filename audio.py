import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()

# Specify the path to your audio file
audio_file_path = 'audio.wav'

# Load the audio file
with sr.AudioFile(audio_file_path) as source:
    # Listen for the data (load audio to memory)
    audio_data = r.record(source)
    # Attempt to recognize the speech in the audio
    try:
        text = r.recognize_google(audio_data)
        print(f"Transcribed text: {text}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
