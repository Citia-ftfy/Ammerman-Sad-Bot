import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import os
import tempfile

# Load the Whisper model
model = whisper.load_model("turbo", device="cuda")

def record_and_transcribe():
    duration = 10  # seconds
    samplerate = 16000  # Whisper prefers 16kHz audio

    while True:
        print("Recording...")
        #print(sd.query_devices()) # List available audio devices
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Save the recording to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            write(temp_audio_file.name, samplerate, audio)
            temp_audio_path = temp_audio_file.name

        print("Transcribing...")
        result = model.transcribe(temp_audio_path)
        print("Transcription:", result["text"])

        # Delete the temporary audio file
       # os.remove(temp_audio_path)

# Start the recording and transcription loop
record_and_transcribe()