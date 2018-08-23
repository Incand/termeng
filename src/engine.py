"""Engine main module to handle timing & events"""

import curses
import numpy as np
import time

from src.termobj import Camera
from src.components import Transform


class Event():
    def __init__(self):
        self.callbacks = []

    def add(self, callback):
        self.callbacks.append(callback)

    def remove(self, callback):
        self.callbacks.remove(callback)

    def invoke(self, *args):
        for _c in self.callbacks:
            _c(*args)


dbg_msgs = []

def debug(msg):
    global dbg_msgs
    dbg_msgs.extend(msg.split('\n'))
    dbg_msgs = dbg_msgs[-5:]
    
# Setup
src = None

def get_aspect_ratio():
    height, width = scr.getmaxyx()
    return width / height

start_event = Event()
update_event = Event()
render_event = Event()
stop_event = Event()

FPS = 10
TIME_DELTA = 1 / FPS
TIME = 0

# TODO Correct world to viewport matrix
MAIN_CAMERA = Camera()


def start():
    global scr, TIME
    scr = curses.initscr()

    start_event.invoke()
    
    try:
        while True:
            time.sleep(TIME_DELTA)
            update_event.invoke()

            scr.erase()
            render_event.invoke(scr)
            height = scr.getmaxyx()[0]
            for i, line in enumerate(dbg_msgs):
                scr.addstr(height - len(dbg_msgs) + i, 0, line)

            scr.refresh()
            TIME += TIME_DELTA
    except KeyboardInterrupt:
        pass

    stop_event.invoke()

