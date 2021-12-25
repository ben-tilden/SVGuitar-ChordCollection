import json
import os
import time
from threading import Thread

import utils.parsers as p
from classes.chord import Chord

def trackThread(thread):
    print("Running...\033[s", end='')

    animation = "|/-\\"
    i = 0
    while thread.is_alive():
        print("\033[u" + animation[i % len(animation)], end="\r")
        i += 1
        time.sleep(0.15)

    print("\33[2KDone!")

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

            isSharpOrFlat = p.parseSharpOrFlat(chordName)

            oldPositions = variation["positions"]
            # there are no chords listed in the source db with multiple fingerings
            # therefore, variation["fingerings"][0] captures everything
            oldFingerings = variation["fingerings"][0]

            key = p.parseKey(chordName, isSharpOrFlat)
            suffix = p.parseSuffix(chordName, isSharpOrFlat)

            highestFret = p.parseHighestFret(oldPositions)
            baseFret = p.parseBaseFret(oldPositions, highestFret)

            positions = p.parsePositions(oldPositions, baseFret)
            fingers = p.parseFingers(oldFingerings)

            barres = p.parseBarres(fingers, positions, baseFret)
            capo = p.parseCapo(barres, positions)

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

trackThread(t1)
