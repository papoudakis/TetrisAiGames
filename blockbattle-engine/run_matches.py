import os
import time
from subprocess import call
from time import sleep

from multiprocessing import Process

def f(i, j):
    call('java -cp bin com.theaigames.blockbattle.Blockbattle  "python ../../TetrisAiGames/StartBot/BotRun.py a"  "python ../../TetrisAiGames/StartBot/BotRun.py b" 2>>err.txt 1>out.txt', shell=True)
    print 'Finished game ' +str(i) + ',' + str(j)
if __name__ == '__main__':
  call('rm err.txt',shell = True)
  for j in range(2):
      for i in range(1):
          p = Process(target=f, args=(i,j,))
          p.start()
      p.join()


