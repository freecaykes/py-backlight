#!/usr/bin/env python
import sys
import termios
import contextlib
import subprocess
import select
import time

import pyxhook
import json

from BrightnessControl import *

defaults = "./resources/keymap.json"

key_index = 0
state = 0

DELTA = 1

brcontrol = None

sequence_held = []
key_controls = []

def printError():
    print "Unable to detect active monitor, run 'xrandr --verbose' on command-line for more info"

#key events
def keyEvent_down(event):
    global sequence_held
    sequence_held.append(event.Key)
    # print sequence_held

    iter = 0
    for control in key_controls:
        execute = all(key in sequence_held for key in control)
        if execute:
            brcontrol.scale_moved((-DELTA)**(iter))
            iter = 0
        else:
            iter += 1

def keyEvent_up(event):
    global sequence_held
    sequence_held.remove(event.Key)

@contextlib.contextmanager
def raw_hex(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        # reset char table when closed
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

def main(brcontrol):
    global key_controls
    with open(defaults) as key_maps:
        controls_json_root = json.load(key_maps)

        for control in controls_json_root:
            keys = []
            print len(controls_json_root)
            for i in range(0, len(controls_json_root)):
                keys.append(controls_json_root[control][i])
                print "i:", i, keys
            key_controls.append(keys)

    keyboard_hook_manager = pyxhook.HookManager()
    keyboard_hook_manager.KeyDown = keyEvent_down
    keyboard_hook_manager.KeyUp = keyEvent_up

    keyboard_hook_manager.HookKeyboard()
    keyboard_hook_manager.start()

    try:
        while 1:
            time.sleep(0.1)
    except (KeyboardInterrupt, EOFError):
        keyboard_hook_manager.cancel()
        printError()


if __name__ == "__main__":
    # new instance of BrightnessControl
    brcontrol = BrightnessControl()
    if(brcontrol.initStatus()):
        # if everything ok, invoke UI and start Gtk thread loop
        main(brcontrol)
    else:
        # error
        printError()
        sys.exit(1)
