from guizero import App, Slider, Text, Picture
from threading import Thread
from time import sleep
import pygame.mixer
from pygame.mixer import Sound
import os

path = os.path.dirname(os.path.abspath(__file__))
bg = 'pink'

class PointlessSlider(Slider):
    def __init__(self, app, n, team):
        super().__init__(app, start=100, end=0, horizontal=False, grid=[n, 1],
                         command=self.slider_changed)
        self.height = 800
        self.width = 100
        self.value = 100
        self.text_color = bg
        self.score = Text(app, size=40, color='yellow', grid=[n, 0])
        self.team = team
        img = '{}/images/{}.png'.format(path, team)
        self.team_img = Picture(app, image=img, grid=[n, 3])

    def slider_changed(self, value):
        self.score.value = value
        if self.team == 'philip':
            print("Changed {} to {}".format(self.team, value))

    def slide_to(self, score):
        try:
            score = int(score)
        except ValueError:
            self.score.text_color = 'red'
            self.score.value = 'X'
            print("Changed {} to {}".format(self.team, 'X'))
            return
        def animate():
            i = 100
            while i > score:
                i -= 1
                self.value = i
                sleep(0.08)
            if score == 0:
                self.score.text_color = 'lime'
                while True:
                    sleep(0.5)
                    self.score.value = ''
                    sleep(0.5)
                    self.score.value = '0'
        thread = Thread(target=animate)
        thread.start()

pygame.mixer.init()
sound = Sound('{}/sounds/pointless_countdown.wav'.format(path))

app = App("Pi-ointless", width=1200, height=1000, layout="grid", bg=bg)

teams = ('lauren', 'maria', 'emily', 'philip',
         'rik', 'matt', 'giustina', 'eva')

sliders = [PointlessSlider(app, n=n, team=team)
           for n, team in enumerate(teams)]

scores = '81 27 46 x 0 91 42 88'.split(" ")
# scores = input("Enter scores: ").split(" ")

sleep(1)
for slider, score in zip(sliders, scores):
    slider.slide_to(score)

sound.play()
app.display()