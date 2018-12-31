# adapted from https://stackoverflow.com/a/34497639/3807967
import os
from enum import Enum

import time


# abstracts platform stuff
def getch():
    if os.name == 'nt':
        from msvcrt import getch
    else:
        # assume linux platform
        from getch import getch

    key = getch.__call__()
    if key == KeyList.ARROW_FLAG:
        key += getch.__call__()
        # append the actual arrow key to the arrow flag so that we know its an arrow and still


    return key


class KeyList:
    ESC = b'\x1b'
    CTRLC = b'\x03'
    ARROW_FLAG = b'\xe0'
    # weird, check msdn vk ref
    FKEY_FLAG = '\x00'


class Arrows:
    # check the implementation of getch to see why it is this way
    LEFT = KeyList.ARROW_FLAG + bytes([75])  # https://stackoverflow.com/a/21017834/3807967
    RIGHT = KeyList.ARROW_FLAG + bytes([77])
    UP = KeyList.ARROW_FLAG + bytes([72])
    DOWN = KeyList.ARROW_FLAG + bytes([80])


class Console:
    CLS = "\x1b[2J\x1b[H"
    FLUSH_STR = " " * 20


class KeyDebouncer:

    def __init__(self, tolerance):
        self.prev_time = time.time()
        self.delta = 0
        self.tolerance = tolerance

    def update(self):
        self.delta = time.time() - self.prev_time
        self.prev_time = self.delta

    def should_filter(self):
        return self.delta <= self.tolerance


class KeyControls(Enum):
    UP = 0x00
    DOWN = 0x01
    LEFT = 0x02
    RIGHT = 0x03
    STOP = 0x04
    SET_SPEED_1 = 0x05
    SET_SPEED_2 = 0x06
    EXIT = 0x07
