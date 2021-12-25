import json
import os
from threading import Thread
import time
import sys

from chord import Chord


def write(text: str):
    sys.stdout.write(text)


def back(range_: int):
    for _ in range(range_):
        sys.stdout.write("\b")

def isSharpOrFlatFunc(chordName):
    if len(chordName) > 1 and (str(chordName)[1] == "#" or str(chordName)[1] == "b"):
        return True
    else:
        return False

def initKey(chordName, isSharpOrFlat):
    return chordName[:2] if isSharpOrFlat else chordName[:1]

def initSuffix(chordName, isSharpOrFlat):
    if len(chordName) == 1:
        suffix = "major"
    elif (not isSharpOrFlat and chordName[1:] == "m") or (isSharpOrFlat and chordName[2:] == "m"):
        suffix = "minor"
    elif isSharpOrFlat:
        suffix = chordName[2:]
    else:
        suffix = chordName[1:]
        
    return suffix

def initHighestFret(positions):
    highestFret = 0

    for position in positions:

        if position == "x":
            continue

        posNumber = int(position)

        if posNumber > highestFret:
            highestFret = posNumber

    return highestFret

def initBaseFret(positions, highestFret):
    base = 1
    lowestFret = 24

    for position in positions:

        if position == "x":
            continue

        posNumber = int(position)

        if posNumber < lowestFret:
            lowestFret = posNumber

    # there is no zero'th fret
    if lowestFret == 0:
        lowestFret = 1
    # chords should have a max range of 6 frets - mostly handled on client
    # but base should be moved to accommodate, given the standard will be 5
    if lowestFret >= 3 or (lowestFret == 2 and highestFret >= 6):
        base = lowestFret

    return base

def initFingers(fingerings):
    return [int(finger) for finger in fingerings]

def initPosition(fretPosition, base):
    return -1 if fretPosition == "x" else 1 + int(fretPosition) - base
   
def initPositions(positions, base):
    return [initPosition(position, base) for position in positions]

def getLastDuplicateIndex(fingerGoal, fingersArr):
    for f in range(len(fingersArr) - 1, -1, -1):
        if fingersArr[f] == fingerGoal:
            return f

def initBarres(fingers, positions, baseFret):

    barres = []

    for i in range(6):

        if fingers[i] == 0:
            continue

        last: int = getLastDuplicateIndex(fingers[i], fingers)

        if last == i:
            continue

        if fingers[i] != fingers[last] or positions[i] != positions[last]:
            continue

        if positions[i] in barres:
            continue

        barres.append(positions[i])

    return barres

def initCapo(barres, positions):

    allStringsPlayed = False if -1 in positions else True
    isLowestFret = True if min(positions) in barres else False

    return True if allStringsPlayed and isLowestFret else False


# the desired output format for each chord is the following:
# {
#   "key":"C",
#   "suffix":"major",
#   "positions":[-1,3,2,0,1,0],
#   "fingers":[0,3,2,0,1,0],
#   "barres":[],
#   "baseFret":1,
#   "highestFret":3
#   "capo": false
# }
def parseChords():
    with open("completeChords.json", "r") as read_file:
        data = json.load(read_file)

    export = {"chords": []}

    for chordName in data:
        for variation in data[chordName]:

            isSharpOrFlat = isSharpOrFlatFunc(chordName)

            oldPositions = variation["positions"]
            # reviewing the source database, there are no chords listed with multiple fingerings
            # therefore, variation["fingerings"][0] captures everything
            oldFingerings = variation["fingerings"][0]

            key = initKey(chordName, isSharpOrFlat)
            suffix = initSuffix(chordName, isSharpOrFlat)

            highestFret = initHighestFret(oldPositions)
            baseFret = initBaseFret(oldPositions, highestFret)

            positions = initPositions(oldPositions, baseFret)
            fingers = initFingers(oldFingerings)

            barres = initBarres(fingers, positions, baseFret)
            capo = initCapo(barres, positions)

            newChord = Chord(
                key, suffix, highestFret, baseFret, positions, fingers, barres, capo
            )

            export["chords"].append(newChord.__dict__)
            

    def writeToFile(fileName):
        if os.path.exists(fileName):
            os.remove(fileName)
        with open(fileName, "w") as outfile:
            json.dump(export, outfile)

    writeToFile("completeChordsFormatted.json")


t1 = Thread(target=parseChords, name="process")
t1.start()

write("loading...")
i = 0
chars = "/—\|"
while t1.is_alive():
    write(chars[i])
    time.sleep(.3)
    i += 1
    if i == len(chars):
        i = 0
    back(1)

back(12)
write("Done!")
