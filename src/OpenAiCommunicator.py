from openai import OpenAI
import os
from dotenv import load_dotenv
from vocalProcessing import record_and_transcribe_once as rato
#from vocalSpeach import speak_text as ste
from testing import returnEmoition2 as reto2
from pythonosc import udp_client
import time
import threading
import argparse


parser = argparse.ArgumentParser("Ammerman Sad Bot OpenAI Communicator")
parser.add_argument("--OSC", type=bool, default=False, help="Enable OSC communication", dest="osc_enabled")
args = parser.parse_args()

ai_state = {"loneliness": 0.5, "joy": 0.2, "fear": 0., "anger": 0.0}

ip = "127.0.0.1"
port = 7000


load_dotenv()  # Load environment variables from .env file
openai_key = os.getenv("OPENAI_KEY")
#openai_key = os.getenv("GORK_KEY")

client = OpenAI(api_key=openai_key)  # Replace with your actual API key
conversation1 = client.conversations.create()
print(conversation1)

def getEmotion(text):
    global ai_state
    print("Analyzing emotion for text:" + text)
    emotion_pipeline = reto2("tyeest")
    print("Pipeline loaded")
    emotions = emotion_pipeline(text)[0]
    print(emotions)
    #print(emotions.get('label'=='sadness'))
    # emotions is a list of dicts like [{'label': 'sadness', 'score': 0.83}, ...]
    dominant_emotion = max(emotions, key=lambda x: x['score'])
    

    for item in emotions:
        if item['label'] == 'sadness':
            ai_state['loneliness'] = item['score']
        elif item['label'] == 'joy':
            ai_state['joy'] = item['score']
        elif item['label'] == 'fear':
            ai_state['fear'] = item['score']
        elif item['label'] == 'anger':
            ai_state['anger'] = item['score']


    # ai_state['loneliness'] = next((item['score'] for item in emotions if item['label'] == 'sadness'), 0.5)
    # ai_state['joy'] = next((item['score'] for item in emotions if item['label'] == 'joy'), 0.2)
    # ai_state['fear'] = next((item['score'] for item in emotions if item['label'] == 'fear'), 0.1)
    # ai_state['anger'] = next((item['score'] for item in emotions if item['label'] == 'anger'), 0.0)

    #p5a.emotion_updater(ai_state)
    #print(dominant_emotion)
    return dominant_emotion

def oscresicve():
    #ss
    pass
    

def oscsend():
    client = udp_client.SimpleUDPClient(ip, port)
    while True:
        client.send_message("/loneliness", ai_state["loneliness"])
        client.send_message("/joy", ai_state["joy"])
        client.send_message("/fear", ai_state["fear"])
        client.send_message("/anger", ai_state["anger"])
        time.sleep(0.1)


# def visualize():
#     print("Starting visualization thread in main")
#     global ai_state
#     #pta5 = p5a.startprocess(ai_state)
#     t = threading.Thread(target=p5visualAgent.startprocess, args=(ai_state), daemon=True)
#     t.start()
#     return t
       
#visualize()
# Start visualization on separate thread




def get_response_from_openai(prompt):
    response = client.responses.create(
    model="gpt-3.5-turbo", #ft:gpt-3.5-turbo-1106:personal::BynUP4Ga
    input=[{"role": "assistant","content": "You are playing a very sad bot, respond to the user with indiference, do not break character, you do not need to help the user in any way"},{"role": "user", "content": prompt}],
    conversation=conversation1.id,
    temperature=1.3
    )
    return response.output[0].content[0].text


def main_thread_loop(function):
    while True:
        text = rato()
        getEmotion(text)
        function(ai_state)
        print("do i get here2?")
        response_text = get_response_from_openai(text)
        #response_text = get_response_from_openai(rato())
        print(response_text)
        #ste(response_text)
        time.sleep(0.1)

def main_loop():
    while True:
        text = rato()
        #print(reto(text))
        getEmotion(text)
        #p5visualAgent.emotionUpdater(ai_state)
        
        #response_text = get_response_from_openai(text)
        
        #print(response_text)
        #ste(response_text)
        time.sleep(0.1)


if __name__ == "__main__":
    #vis_thread = visualize()
    threading.Thread(target=oscsend, args=(), daemon=True).start()

    main_loop()
    