#import pyttsx3
#engine = pyttsx3.init()
#engine.say('hello javier.')
#engine.runAndWait()
from gtts import gTTS
import pygame
file = gTTS('hola javier',"ES")

file.save("aa.mp3")
pygame.init()
au = pygame.mixer.Sound("aa.mp3")
au.play()
