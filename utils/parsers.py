def parseSharpOrFlat(chordName):
    if len(chordName) > 1 and (str(chordName)[1] == "#" or str(chordName)[1] == "b"):
        return True
    else:
        return False

def parseKey(chordName, isSharpOrFlat):
    return chordName[:2] if isSharpOrFlat else chordName[:1]

def parseSuffix(chordName, isSharpOrFlat):
    if len(chordName) == 1 or (isSharpOrFlat and len(chordName) == 2):
        suffix = "major"
    elif (not isSharpOrFlat and chordName[1:] == "m") or (isSharpOrFlat and chordName[2:] == "m"):
        suffix = "minor"
    elif isSharpOrFlat:
        suffix = chordName[2:]
    else:
        suffix = chordName[1:]
        
    return suffix

def parseHighestFret(positions):
    highestFret = 0

    for position in positions:

        if position == "x":
            continue

        posNumber = int(position)

        if posNumber > highestFret:
            highestFret = posNumber

    return highestFret

def parseBaseFret(positions, highestFret):
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

def parseFingers(fingerings):
    return [int(finger) for finger in fingerings]

def parsePosition(fretPosition, base):
    return -1 if fretPosition == "x" else 1 + int(fretPosition) - base
   
def parsePositions(positions, base):
    return [parsePosition(position, base) for position in positions]

def parseBarres(fingers, positions, baseFret):

    def getLastDuplicateIndex(fingerGoal, fingersArr):
        for f in range(len(fingersArr) - 1, -1, -1):
            if fingersArr[f] == fingerGoal:
                return f

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

def parseCapo(barres, positions):

    allStringsPlayed = False if -1 in positions else True
    isLowestFret = True if min(positions) in barres else False

    return True if allStringsPlayed and isLowestFret else False
