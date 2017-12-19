#!/usr/bin/env python

import threading
import curses


# Helper class to read single key from keyboard
class KeyboardThread(threading.Thread):
    lock = threading.Lock()
    key = ''

    def __init__(self):
        threading.Thread.__init__(self)
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(1)
        # self.stdscr.addstr(0,10, "Started curses")
        # self.stdscr.refresh()

    def run(self):
        newKey = ''
        try:
            while (newKey != ord('q')):
                newKey = self.stdscr.getch()
                with self.lock:
                    self.key = newKey
        finally:
            curses.nocbreak()
            self.stdscr.keypad(0)
            curses.echo()
            curses.endwin()

    def getKey(self):
        with self.lock:
            keyToReturn = self.key
            self.key = ''
            return keyToReturn
