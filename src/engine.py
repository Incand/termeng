"""Engine main module to handle timing & events"""

import curses
import numpy as np
import time


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


# Setup
start_event = Event()
update_event = Event()
render_event = Event()
stop_event = Event()

FPS = 60
TIME_DELTA = 1 / FPS

# TODO Correct world to viewport matrix
WORLD2VIEW = np.identity(4)


def start():
    scr = curses.initscr()

    start_event.invoke()
    
    try:
        while True:
            time.sleep(TIME_DELTA)
            update_event.invoke()

            scr.erase()
            render_event.invoke(scr)
            scr.refresh()
    except KeyboardInterrupt:
        pass

    stop_event.invoke()

