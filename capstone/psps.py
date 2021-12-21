# from playsound import playsound
# import os
# os.chdir('C:\py_temp\capstone')

# for i in range(1,10):
#     playsound('sample.wav',block=True)
from pygame import mixer
import os
import time
os.chdir('C:\py_temp\capstone')
for i in range(1,10):
    mixer.init() #Initialzing pyamge mixer
    mixer.music.load('sample.wav') #Loading Music File
    mixer.music.play() #Playing Music with Pygame
    time.sleep(3)
    mixer.music.stop()
