import os
import time
from subprocess import call
from time import sleep

from multiprocessing import Process

def f(i):
    call('java -cp bin com.theaigames.blockbattle.Blockbattle  "python ../../TetrisAiGames/StartBot/BotRun.py "  "python ../../TetrisAiGames/StartBot/BotRun.py a" 2>>err.txt 1>out.txt', shell=True)
    print 'Finished game ' +str(i)
if __name__ == '__main__':
    for i in range(10):
        p = Process(target=f, args=(i,))
        p.start()


