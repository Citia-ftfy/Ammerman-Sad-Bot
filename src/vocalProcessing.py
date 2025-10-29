import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import os
import tempfile
import keyboard  # pip install keyboard
import numpy as np
import time
import torch
import pyttsx3

import threading
from pythonosc import dispatcher
from pythonosc import osc_server

# Load the Whisper model
#torch.load(weights_only=True)
device1 = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("tiny.en", device=device1)
print(f"Using device: {device1}")

osc_recording_event = threading.Event()

def _osc_record_handler(unused_addr, value):
    """
    OSC handler expecting /record <0|1> or /record <False|True>.
    When value is truthy -> start recording (set the event).
    When value is falsy -> stop recording (clear the event).
    """
    try:
        v = int(value)
        if v != 0:
            osc_recording_event.set()
            #print("OSC: record START")
        else:
            osc_recording_event.clear()
            #print("OSC: record STOP")
    except Exception:
        # fallback for boolean-like values
        if str(value).lower() in ("1", "true", "on"):
            osc_recording_event.set()
            #print("OSC: record START")
        else:
            osc_recording_event.clear()
            #print("OSC: record STOP")

def start_osc_server(host="127.0.0.1", port=10001):
    """
    Start a threaded OSC UDP server that listens for /record messages.
    Example messages:
      /record 1  -> start recording
      /record 0  -> stop recording
    Returns the server object (serve_forever runs in a daemon thread).
    """
    disp = dispatcher.Dispatcher()
    disp.map("/kk", _osc_record_handler)

    server = osc_server.ThreadingOSCUDPServer((host, port), disp)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"OSC server started on {host}:{port} (use /record 1 to start, /record 0 to stop)")
    return server


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


def record_and_transcribe_once(osc=False, osc_timeout=None):
    samplerate = 16000  # Whisper prefers 16kHz audio
    print("Ready to record and transcribe...")
 
    if osc:
        print("Waiting for OSC /record 1 to start recording...")
        started = osc_recording_event.wait(timeout=osc_timeout)
        if not started:
            print("OSC start timed out.")
            return None
    else:
        print("Hold SPACE to record and transcribe...")
        keyboard.wait('space')  # Wait for spacebar press

    print("Recording...")
    start_time = time.time()
    recording = []

    # Start recording
    stream = sd.InputStream(samplerate=samplerate, channels=1, dtype='int16')
    stream.start()

    try:
        if osc:
            # Record while OSC event is set
            while osc_recording_event.is_set():
                data, _ = stream.read(1024)
                recording.append(data)
        else:
            # Record while space is pressed
            while keyboard.is_pressed('space'):
                data, _ = stream.read(1024)
                recording.append(data)
    finally:
        # ensure we always stop the stream
        stream.stop()

    duration = time.time() - start_time

    if len(recording) == 0:
        print("No audio recorded.")
        return None

    # Concatenate all chunks
    audio = np.concatenate(recording, axis=0)

    # Determine the speaker folder path (one level above this file)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    speaker_dir = os.path.abspath(os.path.join(current_dir, '..', 'speaker'))
    os.makedirs(speaker_dir, exist_ok=True)

    # Enumerate existing wav files to determine the next index
    existing_files = [f for f in os.listdir(speaker_dir) if f.endswith('.wav')]
    next_index = 1
    if existing_files:
        indices = [int(os.path.splitext(f)[0]) for f in existing_files if os.path.splitext(f)[0].isdigit()]
        if indices:
            next_index = max(indices) + 1

    # Save the recording as a wav file in the speaker folder
    save_path = os.path.join(speaker_dir, f"{next_index}.wav")
    write(save_path, samplerate, audio)
    print(f"Saved recording to {save_path}")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        write(temp_audio_file.name, samplerate, audio)
        temp_audio_path = temp_audio_file.name

    print(f"Transcribing {duration:.2f} seconds of audio...")
    result = model.transcribe(temp_audio_path)
    print("Transcription:", result["text"])

    os.remove(temp_audio_path)
    return result["text"]

print("Vocal processing module loaded.")
# Start the recording and transcription loop
#record_and_transcribe_once()