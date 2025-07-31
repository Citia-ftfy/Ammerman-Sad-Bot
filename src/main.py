#Main python king file from which everything will be run

#Start Imports
from multiprocessing import Process
from runner import draw as draw

if __name__ == "__main__":
    p1 = Process(target=draw, args=("jlel",))
    #p2 = Process(target=draw, args=("jlel2",))
    p1.start()
    #p2.start()
    p1.join()
    #p2.join()