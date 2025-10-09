import torch
from TTS.api import TTS
import os

import simpleaudio as sa

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# List available 🐸TTS models
#print(TTS().list_models())

OUTPUT_PATH = "output.wav"
# Init TTS with the target model name
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
tts.to(device)

def get_speaker_wavs():
    speaker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "speaker"))
    speaker_wavs = [
        os.path.abspath(os.path.join(speaker_dir, f)).replace("\\", "/")
        for f in os.listdir(speaker_dir)
        if f.lower().endswith(".wav")
    ]
    # Print in the requested format
    #speaker_wavs_str = "[{}]".format(", ".join(f'"{w}"' for w in speaker_wavs))
    #print(speaker_wavs_str) 
    return speaker_wavs




def speak_text(text):
      # Path to the folder containing speaker WAV files
    speaker_wavs = get_speaker_wavs()

    tts.tts_to_file(text=text, file_path=OUTPUT_PATH, language="en",speaker_wav=speaker_wavs, emotion="sad", speed=1.0)
    # Here you can add code to play the OUTPUT_PATH audio file if needed
    # For example, using simpleaudio or pydub libraries
    wave_obj = sa.WaveObject.from_wave_file(OUTPUT_PATH)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing
    print(f"Spoken: {text}")
# Run TTS
#tts.tts_to_file(text="This is a test", file_path=OUTPUT_PATH, language="en",speaker="Ana Florence", emotion="sad", speed=1.0)
#speak_text("Hello, I am a sad bot. Please don't leave me alone.")

