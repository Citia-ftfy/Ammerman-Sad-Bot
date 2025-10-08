from openai import OpenAI
import os
from dotenv import load_dotenv
from vocalProcessing import record_and_transcribe_once as rato
from vocalSpeach import speak_text as ste
import pyttsx3
import time

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
    model="gpt-3.5-turbo", #ft:gpt-3.5-turbo-1106:personal::BynUP4Ga
    input=[{"role": "assistant","content": "You are playing a very sad bot, respond to the user with indiference, do not break character, you do not need to help the user in any way"},{"role": "user", "content": prompt}],
    conversation=conversation1.id,
    temperature=1.3
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
    ste(response_text)
    time.sleep(0.1)