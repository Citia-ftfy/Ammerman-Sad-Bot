import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# List available 🐸TTS models
print(TTS().list_models())

OUTPUT_PATH = "output.wav"
# Init TTS with the target model name
tts = TTS(model_name="tts_models/en/ek1/tacotron2", progress_bar=False)
# Run TTS
tts.tts_to_file(text="Hello, how are you, its nice, to meet you", file_path=OUTPUT_PATH)