import json
import os
from threading import Thread
import time
import sys

export = {}


def write(text: str):
    sys.stdout.write(text)


def back(range_: int):
    for _ in range(range_):
        sys.stdout.write("\b")


def reverse(num: int):
    reversedArray = [7, 6, 5, 4, 3, 2, 1]
    return reversedArray[num]


def getLastDuplicateIndex(fingerGoal, fingeringsArray):
    for f in range(len(fingeringsArray) - 1, -1, -1):
        if int(fingeringsArray[f]) == fingerGoal:
            return f


def parseChords():
    with open("completeChords.json", "r") as read_file:
        data = json.load(read_file)
    for key in data:

        export[key] = []

        for variation in data[key]:

            base = 1
            positions = variation["positions"]
            # reviewing the source database, there are no chords listed with multiple fingerings
            # therefore, variation["fingerings"][0] is able to capture everything
            # regex to search for (non-existent) multi-fingering chords:
            # "fingerings":\[\["([0-9]|x)","([0-9]|x)","([0-9]|x)","([0-9]|x)","([0-9]|x)","([0-9]|x)"\]^\]
            fingerings = variation["fingerings"][0]
            lowestFret = 24
            highestFret = 0

            # for loop to set the lowest and highest frets in chart
            for position in positions:

                if position == "x":
                    continue

                posNumber = int(position)

                if posNumber < lowestFret:
                    lowestFret = posNumber

                if posNumber > highestFret:
                    highestFret = posNumber

            # if statement to ensure the chart's base is at the lowest fingered fret if the chord has a wide range
            if highestFret >= 5:
                base = lowestFret

            fingers = []
            barres = []

            # for loop to transform the positions array to the fingers array in SVGuitar
            # the desired output format here mimics the following:
            #    fingers: [
            #        // finger at string 1, fret 2, with text '2'
            #        [1, 2, '2'],

            #        // finger at string 2, fret 3, with text '3', colored red and has class '.red'
            #        [2, 3, { text: '3', color: '#F00', className: 'red' }],

            #        // finger is triangle shaped
            #        [3, 3, { shape: 'triangle' }],
            #        [6, 'x'],
            #    ]
            for i in range(6):

                # prevent finger number from appearing if there are no nuts
                isFretted = True if positions[i] != "x" and positions[i] != "0" else False

                if positions[i] != "x":
                    positions[i] = 1 + int(positions[i]) - base

                payload = [reverse(i + 1), positions[i], fingerings[i]] if isFretted else [reverse(i + 1), positions[i]]

                fingers.append(payload)

            # for loop to extract the barre information from the fingering
            for i in range(6):
                finger = int(fingerings[i])

                if finger == 0:
                    continue

                last: int = getLastDuplicateIndex(finger, fingerings)

                if last == i:
                    continue

                if fingerings[i] != fingerings[last] or positions[i] != positions[last]:
                    continue

                validBarre = True
                for barre in barres:
                    if barre["fret"] == positions[i]:
                        validBarre = False
                        break

                if not validBarre:
                    continue

                barres.append({
                    "fromString": reverse(i) - 1,
                    "toString": reverse(last) - 1,
                    "fret": positions[i]
                })

            fingers.reverse()
            fingersToRemove = []

            for i in range(6):
                for barre in barres:
                    if barre["fret"] == fingers[i][1]:
                        fingersToRemove.append(fingers[i])

            for finger in fingersToRemove:
                fingers.remove(finger)

            # stringifying fingers here because Firestore doesn't allow for nested arrays
            # future state may involve forking SVGuitar to alter the formatting
            newObject = {"title": key, "fingers": json.dumps(fingers), "barres": barres, "position": base}
            export[key].append(newObject)

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
