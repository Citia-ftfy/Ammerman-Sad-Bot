import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import os
import tempfile
import keyboard  # pip install keyboard
import numpy as np
import time
import torch

# Load the Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("tiny.en", device=device)
print(f"Using device: {device}")

def record_and_transcribe():
    samplerate = 16000  # Whisper prefers 16kHz audio

    print("Hold SPACE to record and transcribe...")
    while True:
        keyboard.wait('space')  # Wait for spacebar press
        print("Recording...")
        start_time = time.time()
        recording = []

        # Start recording
        stream = sd.InputStream(samplerate=samplerate, channels=1, dtype='int16')
        stream.start()
        while keyboard.is_pressed('space'):
            data, _ = stream.read(1024)
            recording.append(data)
        stream.stop()
        duration = time.time() - start_time

        # Concatenate all chunks
        audio = np.concatenate(recording, axis=0)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            write(temp_audio_file.name, samplerate, audio)
            temp_audio_path = temp_audio_file.name

        print(f"Transcribing {duration:.2f} seconds of audio...")
        result = model.transcribe(temp_audio_path)
        print("Transcription:", result["text"])

        os.remove(temp_audio_path)

def record_and_transcribe_once():
    samplerate = 16000  # Whisper prefers 16kHz audio

    print("Hold SPACE to record and transcribe...")
    keyboard.wait('space')  # Wait for spacebar press
    print("Recording...")
    start_time = time.time()
    recording = []

    # Start recording
    stream = sd.InputStream(samplerate=samplerate, channels=1, dtype='int16')
    stream.start()
    while keyboard.is_pressed('space'):
        data, _ = stream.read(1024)
        recording.append(data)
    stream.stop()
    duration = time.time() - start_time

    # Concatenate all chunks
    audio = np.concatenate(recording, axis=0)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        write(temp_audio_file.name, samplerate, audio)
        temp_audio_path = temp_audio_file.name

    print(f"Transcribing {duration:.2f} seconds of audio...")
    result = model.transcribe(temp_audio_path)
    print("Transcription:", result["text"])

    os.remove(temp_audio_path)
    return result["text"]

# Start the recording and transcription loop
#record_and_transcribe_once()