import json

class Chord:

    def __init__(
        self, key, suffix, highestFret, baseFret, positions, fingers, barres, capo
    ):

        self.key = key
        self.suffix = suffix
        self.highestFret = highestFret
        self.baseFret = baseFret
        self.positions = positions
        self.fingers = fingers
        self.barres = barres
        self.capo = capo

    def printChord(self):
        print(json.dumps(self.__dict__))
