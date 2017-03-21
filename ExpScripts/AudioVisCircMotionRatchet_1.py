#!/usr/bin/env python2

from __future__ import division # so that division produces float 

__author__ = "Max Smith - mkaillersmith@gmail.com"

from psychopy import visual, logging
import os, sys, random, datetime, time, psychopy
from psychopy import core, data, event, logging, gui
import numpy as np
import math
import pylab
from psychopy import sound

## Preferences Settings ##

# window type = 'pyglet'
# units = 'deg'
# audio library = 'pyo'
# sound driver = ASIO

#Test Sccreen Size
#screenSize = (800, 600)

#Experiment Screen Size 
screenSize = (1600, 900)
win = visual.Window(screenSize, monitor='testMonitor')
#win.setRecordFrameIntervals(True)
allowedKeys = ['space']
#logging.console.setLevel(logging.WARNING)

#Sound Stimulus
in_phase_snd = sound.Sound('10s_whiteNoiseBursts_In_Phase_200.wav')
out_phase_snd = sound.Sound('10s_whiteNoiseBursts_Out_Phase_200.wav')

#Initialize Sounds by playing at low volume
in_phase_snd.setVolume(.01)
in_phase_snd.play()
in_phase_snd.setVolume(1.0)

out_phase_snd.setVolume(.01)
out_phase_snd.play()
out_phase_snd.setVolume(1.0)


## Magic Numbers ##

# Timing
refreshRate = 60 # mkae sure that testing monitor is 60fps 
adaptorTime = 10 # how many seconds should adaptor stimulus play (10s)
ambiguousTime = 20 # how many seconds should ambiguous stimulus play (limit response to 20s)
framesPerStim = 12 # adaptor -- frames per location before movement (4Hz=250ms)
ambiguousFramesPerStim = 12 # ambiguous -- frames per location before movement (4Hz=250ms)
blankTime = 1 # seconds for blank screen to appear
ITI = .5 # inter trial interval (.5s)


## Visual Stimulus Objects ##

# Fixation Cross
fixationRadius_1 = .1
fixationRadius_2 = .3
fixPos = (0,0)
fixationColor = 'red'
fixationResponseColor = 'green'
fixationCircle_1 = visual.Circle(win=win, radius=fixationRadius_1, edges=1200, lineColor=fixationColor, fillColor=fixationColor, pos=fixPos)
fixationCircle_2 = visual.Circle(win=win, radius=fixationRadius_2, edges=1200, lineColor=fixationColor, pos=fixPos)
fixationCircle_3 = visual.Circle(win=win, radius=fixationRadius_1, edges=1200, lineColor=fixationResponseColor, fillColor=fixationResponseColor, pos=fixPos)
fixationCircle_4 = visual.Circle(win=win, radius=fixationRadius_2, edges=1200, lineColor=fixationResponseColor, pos=fixPos)
#fixation = visual.TextStim(win=win, text='+', color=fixationColor, pos=fixPos, height=fixationSize)

# Rotating Circle Values
radius = 8 # radius of outline circle
circleRadius = 1.2 # radius of indivudual circles
circleColor = 'black'

# Large Circle
centerCirclePos = (0,0)
centerCircle = visual.Circle(win=win, radius=radius, edges=1200, lineColor=circleColor, pos=centerCirclePos)


## Rotational Movement Calucaltion ##

# Calculation Values
degreesIncrement = 22.5
radians = math.radians(0)
radianIncrement = math.radians(degreesIncrement)
rotateSpeed = .25
rotateStimLength = 40
ambiguousStimLength = 20

# Calculates Coordinates for Circle Rotation
xList = []
yList = []
for i in range(16):
    radians += radianIncrement
    x = radius*(math.sin(radians))
    y = radius*(math.cos(radians))
    xList.append(x)
    yList.append(y)
#    print 'x', x
#    print 'y', y
xPosList = xList*100
yPosList = yList*100


## Instructions ##
instructions = """You will be presented with circles rotating either clockwise or counter-clockwise.

It is important that you fixate on the bullseye at all times throughout the task.

When the circles rotate around the RED bullseye your task will be to pasively stare at the bullseye.

The circles will dissappear, then reappear rotating in the opposite direction around a GREEN bullseye.

Your task is to press SPACE BAR once you no longer perceive the circles as rotating in the opposite direction of the circles when the RED bullseye was present. 


Please Press Any Key to Begin
"""

## Functions ##

def showInstructions(text): # uses psychopy textStim to show the task instructions
    instructions = visual.TextStim(win, text, pos=(0,0), color='white', height=.7)
    while True:
        instructions.draw()
        win.flip()
        keys = event.getKeys()
        if len(keys)> 0:
            break

def showAdaptor(direction, snd): # Function Creates Adaptor Stimuli -- Takes 2 param (direction = ('clockwise'/'counterClockwise'), snd=('in'/'out'/'no'))
    
    rotateDirection = direction # sets the direction of adator rotation
    playSound = snd # Sets sound (in vs out vs no)
    
    # Circle Objects
    circle1 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor) # circleColor
    circle2 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor)
    circle3 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor)
    circle4 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor)
    
    location = -1 # -1 starts circles at veritcal and horizaontal locations
    
#    clock = core.Clock()
#    startTime = clock.getTime()

    counter=0
    for x in range(adaptorTime):
        for frame in range(refreshRate):
            counter+=1
#            Frame Counter Check
#            print 'frame / framesPerStim = ', frame%framesPerStim
#            print 'frame Num: ', frame
#            print 'i: ', i

#           Changes position of the circles 
            circle1.setPos([xPosList[location], yPosList[location]])
            circle2.setPos([xPosList[location+4], yPosList[location+4]])
            circle3.setPos([xPosList[location+8], yPosList[location+8]])
            circle4.setPos([xPosList[location+12], yPosList[location+12]])
            
            # If frame divided by frames per stim has the remainder of framesPerStim -1 then the circle adavnces in rotation either clockwise or counter clockwise
            if frame%framesPerStim == framesPerStim-1:

                if rotateDirection == 'clockwise':
                    location += 1
                elif rotateDirection == 'counterClockwise':
                    location -= 1
                    
#           Draws visual stimuli to buffer 
            centerCircle.draw()
            fixationCircle_1.draw()
            fixationCircle_2.draw()
            circle1.draw()
            circle2.draw()
            circle3.draw()
            circle4.draw()

            win.flip()  
            if playSound == '1': # 1 = Play in phase sound
                in_phase_snd.play()
                playSound = '3'
            elif playSound == '2': # 2 = Play out phase sound
                out_phase_snd.play()
                playSound = '3'
            elif playSound == '3': # 3 = No sound
                playSound = '3'
    event.clearEvents() # clears all eventts from buffer


def showAmbiguous(): # Function Creates Ambiguous Aftereffect Stimuli
    key_init = 0
    
    location = -1
    RTclock = core.Clock()
    response = {"keys": [],
                "firstKey": None,
                "lastKey": None,
                "duration": 0,
                "timedOut": False,
                "clock": None
                }
    startTime = RTclock.getTime()
    print startTime
    while True:
        
        keys = event.getKeys(keyList=allowedKeys)
        if len(keys) > 0:
            response['duration'] = RTclock.getTime() - startTime
            response["keys"] = keys
            response["firstKey"] = keys[0]
            response["lastKey"] = keys[len(keys)-1]
            break # breaks out of the function

        elif RTclock.getTime() - startTime >= ambiguousTime:
            break
            
        for frame in range(refreshRate):

            pos1 = (xPosList[location], yPosList[location])
            pos2 = (xPosList[location+4], yPosList[location+4])
            pos3 = (xPosList[location+8], yPosList[location+8])
            pos4 = (xPosList[location+12], yPosList[location+12])

            circle1 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos1)
            circle2 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos2)
            circle3 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos3)
            circle4 = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor=circleColor, fillColor=circleColor, pos=pos4)
            

            if frame%ambiguousFramesPerStim == 0: # this switches the ambiguous stimuli the amount of frames that the adator switches
                location += 2
                

            centerCircle.draw()
            fixationCircle_3.draw()
            fixationCircle_4.draw()
            circle1.draw()
            circle2.draw()
            circle3.draw()
            circle4.draw()
            
            win.flip()

    response['clock'] = clock.getTime()
    return response

def showFixCircle():
    for i in range(blankTime):
        for frame in range(refreshRate):
            centerCircle.draw()
            fixationCircle_1.draw()
            fixationCircle_2.draw()
            win.flip()

def showITI():
    for i in range(blankTime):
        for frame in range(refreshRate):
            fixationCircle_1.draw()
            fixationCircle_2.draw()
            win.flip()
    event.clearEvents() # clears all eventts from buffer

def showBreak(counter):
    text = "        Block "+str(counter)+" is over! \n\nPress any key to continue."
    breakText = visual.TextStim(win, text, pos=(0,0), color='white', height=1)
    while True:
        breakText.draw()
        win.flip()
        keys = event.getKeys()
        if len(keys)> 0:
            break

def getTrialOrder(subj): # Retrieves a trial order list based upon the participants subject number
    trialfile = open("C:\Users\Testing_J\Desktop\AudioVisMotionRatchetExp\\TrialOrderLists_AudioVisMotionRatchet\\AudioVisCircMotionRatchet_TrialOrderList"+subj[2]+".txt", 'r')
    trialList = []
    print trialfile
    for line in trialfile:
        trials = line.split()
        trialList.append(trials)
    trialOrder = trialList
    inputTrialFile = "AudioVisCircMotionRatchet_TrialOrderList"+subj[2]+".txt"
    expLength = len(trialOrder)
    return trialOrder, inputTrialFile, expLength

def convertTrialNum(trial):
    if trial < 10:
        trial_num = '00' +str(trial)
    elif trial >=10 and trial < 100:
        trial_num = '0'+ str(trial)
    elif trial >= 100:
        trial_num = trial
    return trial_num


## Experiment Engine ## 

# Creates dialog box to enter subject number, condition, and block info
expName = 'None'  # from the Builder filename that created this script
expInfo = {'Participant': "000"} # 'Participant': "000", 'Condition': '0', 'Block': '0'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit() # user pressed cancel
expInfo['date'] = datetime.datetime.now().strftime("%d-%m-%y\nTime: %H:%M:%S") # add a simple timestamp

if not os.path.isdir('data'):
    os.makedirs('data')

subj = str(expInfo['Participant'])
#con = eval(expInfo['Condition'])
#block = eval(expInfo['Block'])

file_log = "C:\\Testing_J\\AudioVisCircMotionRatchet-master\\logging.txt"


# Import Trial Order
trialOrder, inputTrialFile, expLength = getTrialOrder(subj)

#resume = expInfo['Resuming?']
resume = 0
# Writes experiment information subject log file
if resume == 0:
    print "not resuming"
    log_file = open("data\\AVMotion_subject%s.txt" % (subj), 'w') # subj, con, block)
    log_file.write("Experiment Began: " + datetime.datetime.now().strftime("Experiment Ended: %H:%M:%S\n\n"))
    log_file.write('Total Trials = %i\n' % expLength) # 120 trials
    log_file.write('Input Trial Order File: %s\n' % inputTrialFile)
    log_file.write('In Phase Sound File: %s\n' % ('10s_whiteNoiseBursts_In_Phase_200.wav'))
    log_file.write('Out Phase Sound File: %s\n' % ('10s_whiteNoiseBursts_Out_Phase_200.wav'))
    log_file.write('Visual Movement Timing: %s\n' % ('200 msec'))
    log_file.write('Adaptor Time: %s\n' % (str(adaptorTime)+' sec'))
    log_file.write('\n')
    log_file.write("Trial Rotation Sound RT ElapsedTime\n")
    log_file.close()
    trial_num = 0
elif resume == 1:
    t_log_file = open("data\\AVMotion_subject%s.txt" % (subj, con, block), 'r')
    t_log = t_log_file.readlines()
    t_log_file.close()
    t_log - t_log[-1].split(" ")
    trial_num = int(t_log[0])

# Show Instructions

showInstructions(instructions)

clock = core.Clock()
breakCounter = 1
for trial in trialOrder:
    trial_num +=1
    if trial_num == 31 or trial_num == 61 or trial_num == 91:
        showBreak(breakCounter)
        breakCounter += 1
    if trial == 121: # changed to 300 trials
        core.quit()
    print trial
    trialClock = core.Clock()
    startTrial = trialClock.getTime()
    showAdaptor(trial[0], trial[1])
    showFixCircle()
    response = showAmbiguous()
    showITI()
    trial_correction = convertTrialNum(trial_num)
    print 'Trial Duration = ', trialClock.getTime()-startTrial
    
    log_file = open("data\\AVMotion_subject%s.txt" % (subj), 'a') #(subj, con, block)
    log_file.write('%s %s %s %.6f %.6f\n' % (trial_correction, trial[0], trial[1], response["duration"], response['clock']))
    log_file.close()
#
#pylab.plot(win.frameIntervals)
#pylab.show()
