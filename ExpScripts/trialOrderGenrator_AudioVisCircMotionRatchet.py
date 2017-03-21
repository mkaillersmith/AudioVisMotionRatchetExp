#!/usr/bin/env python2

from __future__ import division # so that division produces float 

__author__ = "Max Smith - mkaillersmith@gmail.com"

import numpy as np
import random

# This script generates trial orders that have each category appear an equal number of times per 15 trials and
# does not allow a category to appear no more than 3 times in a row

totalTrials = 120 # Total trials = 120
blockValue = 30 # total trials per block = 30
maxRepeat = 2 # maximum repeats = 3

blockRandomizer = random.choice([1,2])

if blockRandomizer == 1:
    first = 'clockwise'
    second = 'counterClockwise'
else:
    first = 'counterClockwise'
    second = 'clockwise'


def rawShuffle(blockValue): # shuffles a list containing a, b, and c equally to produce a block
    oneBlock = np.repeat([1, 2, 3], (blockValue/3.0))
    random.shuffle(oneBlock)
    return oneBlock


def shuffleCheck(trialBlockList, maxRepeat): # checks to make sure that list satisfies trial repetition constraint
    global y

    #print trialBlockList
    #print len(trialBlockList)
    reshuffle = 0
    trialCounter = 0
    while True:

        # print trialBlockList
        #
        # print "trial Counter = ", trialCounter
        # print "trial value: ", trialBlockList[trialCounter]
        # print 'maxRepeat value: ', trialBlockList[trialCounter-maxRepeat]
        # print 'maxRepeat - 1 value: ', trialBlockList[trialCounter-(maxRepeat-1)]

        if trialBlockList[trialCounter] == trialBlockList[trialCounter-maxRepeat] and trialBlockList[trialCounter] == trialBlockList[trialCounter-(maxRepeat-1)]:
            random.shuffle(trialBlockList)
            trialCounter = 0


        if trialCounter == len(trialBlockList)-1:
            goodList = trialBlockList
            return goodList

        trialCounter += 1

def trialOrderGenerator(totalTrials, blockValue, maxRepeat):
    # recursive_count = 0
    count = 0
    trialOrder = []
    # print int(totalTrials/blockValue)
    for x in range(int(totalTrials/blockValue)):
        y = rawShuffle(blockValue)  # figure out why is it only returning y sometimes???
        goodList = shuffleCheck(y, maxRepeat)
        trialOrder.append(list(goodList))
        if len(goodList) > 0:
            count += 1
        # print(shuffleCheck(x, maxRepeat))
        # print goodList
    # print trialOrder
    return trialOrder

def trialOrderToTxt(trialOrder, listNum):
#    blockList = np.repeat([1, 2],30)
    blockCounter = 0
    trialOrderList = []
    trialOrderTxt = open('C:\Users\Testing_J\Desktop\AudioVisMotionRatchetExp\TrialOrderLists_AudioVisMotionRatchet\\AudioVisCircMotionRatchet_TrialOrderList'+str(listNum)+'.txt', 'w')
    for trialList in trialOrder:
        for trial in trialList:
            block = first # counter balance  between subjects
#            if blockCounter < blockValue: # counter balance rotation within subject
#                block = first
#            else:
#                block = second
            trialOrderList.append(trial)
            trialOrderTxt.write('%s %i\n' % (block, trial))
            blockCounter += 1
    trialOrderTxt.close()
    print trialOrderList
    print len(trialOrderList) # make sure to check that it does not appear more than three times in a row


trialOrder = trialOrderGenerator(totalTrials, blockValue, maxRepeat)
trialOrderToTxt(trialOrder,1)
in_phase_lst = []
out_phase_lst = []
no_sound_lst = []
for lst in trialOrder:
    for i in lst:
        print i
        if i == 1:
            in_phase_lst.append('in')
        elif i == 2:
            out_phase_lst.append('out')
        elif i == 3:
            no_sound_lst.append('no')
    print 'in_phase = ', len(in_phase_lst)
    print 'out_phase = ', len(out_phase_lst)
    print 'no = ', len(no_sound_lst)