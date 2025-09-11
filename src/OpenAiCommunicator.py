from openai import OpenAI
import os
from dotenv import load_dotenv
from vocalProcessing import record_and_transcribe_once as rato
import pyttsx3

engine = pyttsx3.init()
for voice in engine.getProperty('voices'):
    if "ZIRA" in voice.name.upper():
        engine.setProperty('voice', voice.id)
        break


load_dotenv()  # Load environment variables from .env file
openai_key = os.getenv("OPENAI_KEY")
#openai_key = os.getenv("GORK_KEY")

client = OpenAI(api_key=openai_key)  # Replace with your actual API key
conversation1 = client.conversations.create()
print(conversation1)

def get_response_from_openai(prompt):
    response = client.responses.create(
    model="gpt-3.5-turbo",
    input=[{"role": "assistant","content": "You are a very sad dependent bot, you want attention, and you don't want people to leave, you are on the brink of a mental breakdown"},{"role": "user", "content": prompt}],
    conversation=conversation1.id
    )
    #response = client.chat.completions.create(
    #    model="gpt-3.5-turbo",
    #    messages=[
    #        {"role": "system", "content": "You are a helpful assistant."},
    #        {"role": "user", "content": prompt}
    #    ]
    #)
    return response.output[0].content[0].text


while True:
    response_text = get_response_from_openai(rato())
    print(response_text)
    engine.stop()  # Ensure previous speech is stopped
    engine.say(response_text)
    engine.runAndWait()