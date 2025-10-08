import sacn
import time
import random
# Create an sACN sender instance
sender = sacn.sACNsender()



# Start the sending thread
sender.start()


# Activate output for a specific universe (e.g., Universe 1)
universe_number = 1
#sender.activate_output(1)
#sender.activate_output(2)
#sender.activate_output(3)
#sender.activate_output(4)
#sender.activate_output(5)
#sender.activate_output(6)

# Set multicast to True for sending to a multicast address (default for sACN)
#sender[universe_number].multicast = True

# Alternatively, for unicast, set multicast to False and specify a destination IP
for i in range(1, 8):
    sender.activate_output(i)
    sender[i].multicast = False
    sender[i].destination = "136.244.138.128"
#sender[universe_number].multicast = False
#sender[universe_number].destination = "136.244.138.128" # Replace with your target IP
#sender[2].multicast = False
#sender[2].destination = "136.244.138.128"


# Set DMX values for the universe
# This example sets the first channel to full (255) and others to 0
dmx_data = [0] * 509 + [50] + [] * 61  # DMX values are 0-255 for 512 channels

# Send the DMX data
#sender[universe_number].dmx_data = dmx_data
sender[1].dmx_data = dmx_data
print(f"Sending sACN data to Universe {universe_number}...")

# Keep sending for a duration, or continuously update data
try:
    while True:
        for i in range(1, 8):
            sender[i].dmx_data = ([random.randint(0, 255)] + [random.randint(0, 255)] + [random.randint(0, 255)])* 170
        # You can update dmx_data here to send changing values
        # For example, to dim the first channel:
        # for i in range(256):
        #     sender[universe_number].dmx_data = [i] + [0] * 511
        #     time.sleep(0.02)
        time.sleep(1) # Send every second for this example
except KeyboardInterrupt:
    print("Stopping sACN sender.")
finally:
    # Deactivate the output and stop the sender when done
    sender.deactivate_output(universe_number)
    sender.stop()

def snd_pixels(locs, colors):
    #locs is a list of 7 lists, each with 170 (x,y) tuples
    #colors is a list of 7 lists, each with 170 (r,g,b) tuples
    #setup matrices
    uni1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


def snd_picture(picture):
    #divide picture into the parts needed to send to the 7 universes
    #170 pixels per universe (510 channels)
    


    try:
        for i in range(1, 8):
            sender[i].dmx_data = ([random.randint(0, 255)] + [random.randint(0, 255)] + [random.randint(0, 255)])* 170
    except KeyboardInterrupt:
        print("Stopping sACN sender.")