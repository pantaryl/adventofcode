import os
import __main__

_MAIN_FILE        =__main__.__file__
_MAIN_DIR         = os.path.dirname(_MAIN_FILE)
_MAIN_FILE_NO_EXT = os.path.splitext(os.path.basename(_MAIN_FILE))[0]

INPUT_DATA = []
with open(f"{_MAIN_DIR}/../input/{_MAIN_FILE_NO_EXT}.txt", 'r') as inputFile:
    INPUT_DATA = [x.rstrip() for x in inputFile.readlines()]