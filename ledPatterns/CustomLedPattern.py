#!/usr/bin/env python
# -*- coding: utf-8 -*-

from respeaker.apa102 import APA102
import time
import respeaker.pixels


class CustomLedPattern(object):
    def __init__(self, pixels, num_leds=3, show=False):

        self._leds      = APA102(num_led=num_leds)
        self._pixels    = pixels #type: respeaker.pixels.Pixels

        self._numLeds   = num_leds
        self.stop       = False

    #_________________animation functions to use in states functions:
    def breathLeds(self, duration=1, color=[0,0,40], leds=[]): #smootly light up and down, all or specified leds by numbers. By KiboOst
        if len(leds) == 0:
            leds = [i for i in range(self._numLeds)]

        pause = float(duration/200.00)
        direction = 1
        brightness = 0

        frame = 0
        while frame < duration:
            if self.stop: return
            for l in leds:
                self._leds.set_pixel(l, color[0], color[1], color[2], brightness)
            self._leds.show()

            time.sleep(pause)

            if brightness <= 0:
                direction = 1
            elif brightness >= 100:
                direction = -1

            brightness += direction
            frame += pause
    #

    def tailTranslate(self, duration=0.5, color=[0,0,40,0], invert=False): #progressive translation of all leds. By KiboOst
        pause = float(duration / (self._numLeds*2))
        step = int(100/self._numLeds+1)

        for i in range(self._numLeds):
            self._leds.set_pixel(i, color[0], color[1], color[2], 0)
        self._leds.show()

        refs = [0 for i in range(self._numLeds)]
        refs[0] = 100

        for i in range(self._numLeds):
            if self.stop: return
            for j in range(i, 0, -1):
                if refs[j] >= step:
                    refs[j-1] = refs[j] - step
                else:
                    refs[j-1] = 0

            if invert: refs = list(reversed(refs))
            for l in range(self._numLeds):
                self._leds.set_pixel(l, color[0], color[1], color[2], refs[l])
            self._leds.show()
            if invert: refs = list(reversed(refs))
            time.sleep(pause)
            refs.pop()
            refs.insert(0, 0)

        for i in range(self._numLeds):
            if self.stop: return
            if invert: refs = list(reversed(refs))
            for l in range(self._numLeds):
                self._leds.set_pixel(l, color[0], color[1], color[2], refs[l])
            self._leds.show()
            if invert: refs = list(reversed(refs))
            refs.pop()
            refs.insert(0, 0)
            time.sleep(pause)
    #

    def translate(self, duration=0.5, color=[0,0,40,0], leds=[], invert=False): #translation of specified leds. By KiboOst
        if len(leds) == 0:
            leds = [int(self._numLeds/2)]

        pause = float(duration / (self._numLeds+1))
        refs = [0 for i in range(self._numLeds)]

        for i in range(self._numLeds):
            if i in leds:
                refs[i] = 100

        for i in range(self._numLeds+1):
            if self.stop: return
            if invert: refs = list(reversed(refs))
            for l in range(self._numLeds):
                self._leds.set_pixel(l, color[0], color[1], color[2], refs[l])
            self._leds.show()
            if invert: refs = list(reversed(refs))
            time.sleep(pause)
            refs.pop()
            refs.insert(0, 0)
    #

    #_________________states functions:
    def wakeup(self, direction=0, *args):
        self._leds.clear_strip()
        self.tailTranslate(0.3, [100,0,0])
        self.tailTranslate(0.3, [100,0,0], True)
        self._leds.clear_strip()

    def listen(self, *args):
        self._leds.clear_strip()
        while not self.stop:
            self.tailTranslate(0.5, [0,0,100])
            self.tailTranslate(0.5, [0,0,100], True)

        self._leds.clear_strip()


    def think(self, *args):
        self._leds.clear_strip()
        while not self.stop:
            self.tailTranslate(0.3, [100,60,5])
            self.tailTranslate(0.3, [100,60,5], True)

        self._leds.clear_strip()


    def speak(self, *args):
        self._leds.clear_strip()

        leds = [i for i in range(self._numLeds)]
        del leds[int(self._numLeds/2)]
        while not self.stop:
            #self.breathLeds(0.3, [0,0,90], leds)
            self.tailTranslate(0.5, [0,100,0])
            self.tailTranslate(0.5, [0,100,0], True)

        self._leds.clear_strip()


    def idle(self, *args):
        self._leds.clear_strip()

        while not self.stop:
            self.breathLeds(1, [0,0,60])

        self._leds.clear_strip()

    def onError(self, *args):
        self._leds.clear_strip()
        for i in range(self._numLeds):
            self._leds.set_pixel(i, 120, 0, 0, 100)
        self._leds.show()
        time.sleep(0.5)
        self._leds.clear_strip()


    def onSuccess(self, *args):
        self._leds.clear_strip()
        for i in range(self._numLeds):
            self._leds.set_pixel(i, 0, 120, 0, 100)
        self._leds.show()
        time.sleep(0.5)
        self._leds.clear_strip()


    def off(self, *args):
        self._leds.clear_strip()
