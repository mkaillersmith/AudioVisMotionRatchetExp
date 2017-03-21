#!/usr/bin/env python2

__author__ = "Max Smith - mkaillersmith@gmail.com"

## This is code for a fixation training exercise ##

import numpy as np 
from psychopy import visual, event, core
from numpy import random


from psychopy import visual, logging




## Setting ##
# create a window
win = visual.Window([512, 512], monitor="testMonitor", units="deg", screen=1, color=-1, fullscr=True) # background set to black
win.setRecordFrameIntervals(True)
win._refreshThreshold=1/60.0+0.004 #i've got 60Hz monitor and want to allow 4ms tolerance

#set the log module to report warnings to the std output window (default is errors only)
#logging.console.setLevel(logging.WARNING)

timeSecs =3
maskDuration = 5 # Duration of mask in secs
refreshRate = 60 # screeb refresh rate
frameSwitch = 1 # change nosie texture every frame (16.6666667 msec per frame)
visualNoiseSize =512 # Dimension in pixels of visual noise. Must be a power of 2
noiseSize = 512

choices = [-1,1] # sets to high contrast (-1 = black, 1 = white)
noiseTexture = np.zeros((visualNoiseSize, visualNoiseSize)) # creates an 512*512 array of all zeros
noiseTexture2 = np.zeros((visualNoiseSize, visualNoiseSize))

fixInterval = 30 # of fixation intervals

## Functions ##
def makeFixationArray(noiseTex):
    for i in noiseTex: # 0 - 511 -- there are 512 rows 
        for x in range(len(i)):
            i[x] = random.choice(choices)
    return noiseTex

def makeInverseFixationArray(noiseTex, noiseTex2):
    for i in range(len(noiseTex)): # 0 - 511 -- there are 512 rows 
        for x in range(len(noiseTex)):
            if noiseTex[i][x] >0:
                noiseTex2[i][x] = -1
            else:
                noiseTex2[i][x] = 1
    return noiseTex2

def showInstructions(text, num): # uses psychopy textStim to show the task instructions
    instructions = visual.TextStim(win, text+str(num), pos=(0,0), color='white', height=.7)
    while True:
        instructions.draw()
        win.flip()
        keys = event.getKeys()
        if len(keys)> 0:
            break

instructions='Fixation Trainer:  '

## create arrays of black and white pixels ##
texture1 = makeFixationArray(noiseTexture)
texture2 = makeInverseFixationArray(texture1, noiseTexture2)

# Random dot object
visualNoise1 = visual.GratingStim(win=win, tex=texture1, size=(visualNoiseSize,visualNoiseSize), units='pix',interpolate=False, mask='raisedCos')

## Fixation Stimulus ##
fixationRadius_1 = .1
fixationRadius_2 = .3
fixPos = (0,0)
fixationColor = 'red'

fixationCircle_1 = visual.Circle(win=win, radius=fixationRadius_1, edges=1200, lineColor=fixationColor, fillColor=fixationColor, pos=fixPos)
fixationCircle_2 = visual.Circle(win=win, radius=fixationRadius_2, edges=1200, lineColor=fixationColor, pos=fixPos)

## Engine ##
# Switches back and forth between textures on each screen refresh 
for i in range(fixInterval):

    showInstructions(instructions, i+1)

    for secs in range(maskDuration):
        for frame in range(refreshRate):

            
            if frame%2 == 0:
                visualNoise1.setTex(texture1)
            
            else:
                visualNoise1.setTex(texture2)
            visualNoise1.draw()
        
            fixationCircle_1.draw()
            fixationCircle_2.draw()

            win.flip()
core.quit()
