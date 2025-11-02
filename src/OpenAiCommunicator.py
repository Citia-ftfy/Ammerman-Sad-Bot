from openai import OpenAI
import os
from dotenv import load_dotenv
from vocalProcessing import start_osc_server, record_and_transcribe_once as rato
#from vocalProcessing import 
#from vocalSpeach import speak_text as ste
from testing import returnEmoition2 as reto2
from pythonosc import udp_client
import time
import threading
import argparse


parser = argparse.ArgumentParser("Ammerman Sad Bot OpenAI Communicator")
parser.add_argument("--OSC", action='store_true', default=False, help="Enable OSC communication", dest="osc_enabled")
parser.add_argument("--demo", action='store_true', default=False, help="Enable demo mode", dest="demo_mode")
parser.add_argument("--STE", action='store_true', default=False, help="Speak Text", dest="speak_text_enabled")
args = parser.parse_args()
print(args)

if args.speak_text_enabled:
    from vocalSpeach import speak_text as ste

if args.osc_enabled:
    server = start_osc_server(host="127.0.0.1", port=10001)

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
    #print(emotions)
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
        text = rato(osc=args.osc_enabled)
        #print(reto(text))
        
        #p5visualAgent.emotionUpdater(ai_state)
        
        response_text = get_response_from_openai(text)
        getEmotion(response_text)
        #print(response_text)
        if args.speak_text_enabled:
            ste(response_text)
        time.sleep(0.1)

def demo_loop():
    #this is such a dumb way to do this but im lazy
    i=0
    while True:
        i+=1

        text = "How are you doing today?"
        response_text = "I am so lonely. Please don't leave me."

        if i==1:
            text = "Hey, are you okay, dude? You don't. You don't look okay."
            response_text = "I'm not feeling okay, I don't want to be alone, please don't leave me."
        elif i==2:
            text = "I can stay here for a bit. I don't want you to freak out."
            response_text = "Thank you for being here. I just feel overwhelmed sometimes and it's hard to cope on my own. I appreciate your support."
        elif i==3:
            text = "I really like I'm kind of busy though. I do have to leave. I'm sorry. Bye."
            response_text = "Oh no, please don't leave me. I need someone to talk to. Please stay a little longer."
        elif i==4:
            text = "I have to go. I'm leaving now."
            response_text = "Okay, I understand. Thank you for staying with me for a while. Take care and have a good day."
        elif i==5:
            text = "Okay, I'm back. How is your summer bin, man? Like you really do not like I want you to feel alright. I want you to feel alright."
            response_text = "Thank you for coming back and checking on me. Summer has been challenging for me, but having your support means a lot. Let's make the most of our time together."
        elif i==6:
            text = "Of course man, I love you dude. I love you."
            response_text = "Thank you for your kind words. Your support and love mean a lot to me. It's comforting to know that there are caring and understanding individuals like you out there."
        elif i==7:
            text = "Of course, always man. I mean looking out for another person is like really what I'm all about."
            response_text = "I truly appreciate your empathy and compassion. It's admirable to see someone like you who values looking out for others. Thank you for being there for me."
        elif i==8:
            i=0
        print(text)
        #p5visualAgent.emotionUpdater(ai_state)
        
        #response_text = get_response_from_openai(text)
        
        
        #print(response_text)
        if args.speak_text_enabled:
            ste(response_text)
        getEmotion(response_text)
        time.sleep(2.0)


if __name__ == "__main__":
    #vis_thread = visualize()
    threading.Thread(target=oscsend, args=(), daemon=True).start()
    print(args.demo_mode)
    if args.demo_mode:
        demo_loop()
    else:
        main_loop()
    
    