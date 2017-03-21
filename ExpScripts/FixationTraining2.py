#!/usr/bin/env python2

__author__ = "Max Smith - mkaillersmith@gmail.com"

## This is code for a fixation training exercise ##

import numpy as np 
from psychopy import visual, event
from numpy import random

## Setting ##
# create a window
win = visual.Window([1600, 900], monitor="testMonitor", units="deg", color=-1, screen=2, fullscr=True) # background set to black

maskDuration = 20 # Duration of mask in secs
refreshRate = 60 # screen refresh rate
frameSwitch = 1 # change nosie texture every frame (16.6666667 msec per frame)
visualNoiseSize = 512 # Dimension in pixels of visual noise. Must be a power of 2
noiseSize = 512
rowlist = np.repeat([-1,1],noiseSize/2)

def makeFixationArray():
    noiseTex = []
    for i in range(512):
        random.shuffle(rowlist)
        noiseTex.append(rowlist)
    return noiseTex
#choices = [-1.0,1.0] # sets to high contrast (-1 = black, 1 = white)
#noiseTexture = np.zeros((visualNoiseSize, visualNoiseSize)) # creates an 512*512 array of all zeros
#
## Functions ##

#    for i in range(512): # 0 - 511 -- there are 512 rows 
#            noiseTex[i][x] = random.choice(choices)
#    
#
def makeInverseFixationArray(noiseTex):
    noiseTex2 = np.zeros((visualNoiseSize, visualNoiseSize))
    for i in range(512): # 0 - 511 -- there are 512 rows 
        for x in range(512):
            if noiseTex[i][x] == 1:
                noiseTex2[i][x] = -1
            elif noiseTex[i][x] == -1:
                noiseTex2[i][x] = 1
    return noiseTex2
#
## create arrays of black and white pixels ##
texture1 = makeFixationArray()
texture2 = makeInverseFixationArray(texture1)
#print texture1[0][0]
#print texture2[0][0]#
visualNoise1 = visual.GratingStim(win=win, tex=texture2, size=(visualNoiseSize,visualNoiseSize), units='pix',interpolate=True, mask='gauss')
visualNoise2 = visual.GratingStim(win=win, tex=texture2, size=(visualNoiseSize,visualNoiseSize), units='pix',interpolate=True, mask='gauss')

## Fixation Stimulus ##
fixationRadius_1 = .1
fixationRadius_2 = .3
fixPos = (0,0)
fixationColor = 'red'
fixationResponseColor = 'green'
fixationCircle_1 = visual.Circle(win=win, radius=fixationRadius_1, edges=1200, lineColor=fixationColor, fillColor=fixationColor, pos=fixPos)
fixationCircle_2 = visual.Circle(win=win, radius=fixationRadius_2, edges=1200, lineColor=fixationColor, pos=fixPos)
fixationCircle_3 = visual.Circle(win=win, radius=fixationRadius_1, edges=1200, lineColor=fixationResponseColor, fillColor=fixationResponseColor, pos=fixPos)
fixationCircle_4 = visual.Circle(win=win, radius=fixationRadius_2, edges=1200, lineColor=fixationResponseColor, pos=fixPos)

## Engine ##
# Switches back and forth between textures on each screen refresh 
show = 1


switch = 0
frameCounter = 0
if show ==1:
    while True:
        keys = event.getKeys()
        if len(keys)>0:
            break

        if frameCounter%frameSwitch == 0:
            switch += 1
                
            if switch%2 == 0:
                visualNoise1.draw()
            else:
                visualNoise2.draw()
            fixationCircle_1.draw()
            fixationCircle_2.draw()

            win.flip()
        frameCounter += 1

