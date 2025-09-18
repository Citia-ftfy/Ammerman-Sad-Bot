import torch
from TTS.api import TTS

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
# Run TTS
#tts.tts_to_file(text="This is a test", file_path=OUTPUT_PATH, language="en",speaker="Ana Florence", emotion="sad", speed=1.0)

def speak_text(text):
    tts.tts_to_file(text=text, file_path=OUTPUT_PATH, language="en",speaker="Ana Florence", emotion="sad", speed=1.0)
    # Here you can add code to play the OUTPUT_PATH audio file if needed
    # For example, using simpleaudio or pydub libraries
    wave_obj = sa.WaveObject.from_wave_file(OUTPUT_PATH)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing
    print(f"Spoken: {text}")