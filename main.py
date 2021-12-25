import json
import os
from threading import Thread
import time
import sys

export = {"chords": []}


def write(text: str):
    sys.stdout.write(text)


def back(range_: int):
    for _ in range(range_):
        sys.stdout.write("\b")

def isSharpOrFlatFunc(key):
    if len(key) > 1 and (str(key)[1] == "#" or str(key)[1] == "b"):
        return True
    else:
        return False

def setKey(key, isSharpOrFlat):
    return key[:2] if isSharpOrFlat else key[:1]

def setSuffix(key, isSharpOrFlat):
    if len(key) == 1:
        suffix = "major"
    elif (not isSharpOrFlat and key[1:] == "m") or (isSharpOrFlat and key[2:] == "m"):
        suffix = "minor"
    elif isSharpOrFlat:
        suffix = key[2:]
    else:
        suffix = key[1:]
        
    return suffix

def setHighestFret(positions):
    highestFret = 0

    for position in positions:

        if position == "x":
            continue

        posNumber = int(position)

        if posNumber > highestFret:
            highestFret = posNumber

    return highestFret

def setBaseFret(positions, highestFret):
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

def setFingers(fingerings):
    return [int(finger) for finger in fingerings]

def setPosition(fretPosition, base):
    return -1 if fretPosition == "x" else 1 + int(fretPosition) - base
   
def setPositions(positions, base):
    return [setPosition(position, base) for position in positions]

def getLastDuplicateIndex(fingerGoal, fingeringsArray):
    for f in range(len(fingeringsArray) - 1, -1, -1):
        if int(fingeringsArray[f]) == fingerGoal:
            return f

def setBarres(fingerings, positions):

    barres = []

    for i in range(6):
        finger = int(fingerings[i])

        if finger == 0:
            continue

        last: int = getLastDuplicateIndex(finger, fingerings)

        if last == i:
            continue

        if fingerings[i] != fingerings[last] or positions[i] != positions[last]:
            continue

        position = int(positions[i])

        if position in barres:
            continue

        barres.append(position)

    return barres

def setCapo(barres, positions, base):

    base = 0 if '0' in positions else base

    allStringsPlayed = False if 'x' in positions else True
    isLowestFret = True if base in barres else False

    return True if allStringsPlayed and isLowestFret else False


# the desired output format for each chord is the following:
# {
#   "key":"C",
#   "suffix":"major",
#   "frets":[-1,3,2,0,1,0],
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

    for key in data:
        for variation in data[key]:

            newChord = {}

            isSharpOrFlat = isSharpOrFlatFunc(key)

            positions = variation["positions"]
            # reviewing the source database, there are no chords listed with multiple fingerings
            # therefore, variation["fingerings"][0] captures everything
            fingerings = variation["fingerings"][0]

            newChord["key"] = setKey(key, isSharpOrFlat)
            newChord["suffix"] = setSuffix(key, isSharpOrFlat)
            newChord["highestFret"] = setHighestFret(positions)
            newChord["baseFret"] = setBaseFret(positions, newChord["highestFret"])
            newChord["frets"] = setPositions(positions, newChord["baseFret"])
            newChord["fingers"] = setFingers(fingerings)
            newChord["barres"] = setBarres(fingerings, positions)
            newChord["capo"] = setCapo(newChord["barres"], positions, newChord["baseFret"])

            export["chords"].append(newChord)
            

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
