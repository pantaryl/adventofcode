from collections import Counter, defaultdict, deque
from helpers import memoize
from copy import deepcopy
from enum import Enum
import os
from .math_utils import *
from .helpers    import *

import __main__

_MAIN_FILE        =__main__.__file__
_MAIN_DIR         = os.path.dirname(_MAIN_FILE)
_MAIN_FILE_NO_EXT = os.path.splitext(os.path.basename(_MAIN_FILE))[0]

# Complex numbers in Python! == i + nj (x + ny), good for coordinates
# complex*+imaginary to rotate left/ccw, complex*-imaginary to rotate right/cw
# For example:
# Rotate CCW by 270 degrees:
#    val *= complex(0, 1) ** 3 [each power represents 90 degrees]

INPUT_DATA = []
with open(f"{_MAIN_DIR}/../input/{_MAIN_FILE_NO_EXT}.txt", 'r') as inputFile:
    INPUT_DATA = [x.rstrip() for x in inputFile.readlines()]