from guizero import App, Slider, Text, Picture
from threading import Thread
from time import sleep
import pygame.mixer
from pygame.mixer import Sound

class PointlessSlider(Slider):
    def __init__(self, app, n):
        super().__init__(app, start=100, end=0, horizontal=False, grid=[n, 1], command=self.slider_changed)
        self.height = 800
        self.width = 100
        self.value = 100
        self.text_color ='pink'
        self.score = Text(app, size=40, color='yellow', grid=[n, 0])
        self.team_img = Picture(app, image='images/ben.png', grid=[n, 3])
        
    def slider_changed(self, value):
        self.score.value = value
        
    def slide_to(self, n):
        if n is None:
            self.score.text_color = 'red'
            self.score.value = 'X'
            return
        i = 100
        while i > n:
            i -= 1
            self.value = i
            sleep(0.08)
            
def check_score(score):
    try:
        return int(score)
    except ValueError:
        return None
        
pygame.mixer.init()
sound = Sound('sounds/pointless_countdown.wav')

app = App("Pi-ointless", width=1200, height=1000, layout="grid", bg='pink')

sliders = [PointlessSlider(app, n=i) for i in range(8)]

scores = '81 27 46 x 0 91 42 88'.split(" ")  # scores = input("Enter scores: ").split(" ")

threads = [Thread(target=slider.slide_to, args=(check_score(score), )) for slider, score in zip(sliders, scores)]
for thread in threads:
    thread.start()

sound.play()

app.display()