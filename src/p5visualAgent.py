from p5 import *
import math
import threading
import OpenAiCommunicator as oac

# This dictionary can be updated externally
_emotion_state = {"loneliness": 0.5, "joy": 0.2, "fear": 0.0, "anger": 0.0}

_emotion_lock = threading.Lock()

def setup():
    width = 800
    height = 600
    size(800, 600)
    no_stroke()

def draw():
    global _emotion_state
    background(10)
    width = 800
    height = 600

    # Read emotion state
    loneliness = _emotion_state.get("loneliness", 0.5)
    joy = _emotion_state.get("joy", 0.0)
    anger = _emotion_state.get("anger", 0.0)

    # Map loneliness to orb size and color intensity
    base_size = 150 + loneliness * 300
    pulse_speed = 1 + joy * 3
    t = millis() / 1000.0
    pulse = math.sin(t * pulse_speed * 2 * math.pi) * 0.5 + 0.5

    # Color: sadness = blue, joy = warm, anger = red
    r = int(255 * (anger + 0.2*joy))
    g = int(100 + 155 * joy)
    b = int(255 * (loneliness + 0.2))

    fill(r, g, b, 180)
    ellipse(200, 200, 50, 50)
    ellipse((width/2, height/2), base_size * (0.8 + 0.2 * pulse), base_size * (0.8 + 0.2 * pulse))

    # Optional: text overlay
    fill(255)
    text_align("CENTER", "CENTER")
    #text_size(20)
    text(f"loneliness: {loneliness:.2f}", (width/2, height - 50))

def emotion_updater(ai_state):
    """This simulates your other process that changes emotion over time."""
    global _emotion_state
    #while True:
    print("I am getting stuck here?")
    with _emotion_lock:
         _emotion_state = ai_state


# Run the sketch
def startprocess(ai_state):
    print("Starting p5 visualizer in p5visualAgent")
    global _emotion_state
    _emotion_state = ai_state
    run()

if __name__ == '__main__':
    t = threading.Thread(target=oac.main_thread_loop, args=(emotion_updater,), daemon=True)
    t.start()


    run()