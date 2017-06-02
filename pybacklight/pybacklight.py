#!/usr/bin/env python

import sys
import termios
import contextlib
import subprocess
import select
import time
import collections
from sets import Set
import json

import pyxhook

from BrightnessControl import *

defaults = "./resources/keymap.json"

DELTA = 1.0

sequence_held = Set([])
key_controls_bdown = None   #  init as set in main()
key_controls_bup = None

brcontrol = None
notification_controller = None

def printError():
    print "Unable to detect active monitor, run 'xrandr --verbose' on command-line for more info"

############## key events ##############
def keyEvent_down(event):
    global sequence_held
    iter = 0
    execute_down = ( len(sequence_held.symmetric_difference( key_controls_bdown )) == 0)
    # print "Diff:", sequence_held.symmetric_difference( key_controls_bdown )
    # \
    #                 or ( ( event.Key in key_controls_bdown ) ) #  held keys
    execute_up = ( len(sequence_held.symmetric_difference( key_controls_bup )) == 0)
    # print "Diff:", sequence_held.symmetric_difference( key_controls_bup )
    # \
    #                 or ( (event.Key in key_controls_bup ) )

    sequence_held.add(event.Key)

    print str(sequence_held), execute_up, execute_down

    if execute_down:
        level = (-1)*(DELTA)**(iter)
        brcontrol.scale_moved(  level )
        print "level:", brcontrol.currB
        notification_controller.set_volume_bar( brcontrol.currB )
        notification_controller.show_notification()
        iter = 0
    elif execute_up:
        level = (DELTA)**(iter)
        brcontrol.scale_moved( level )
        print "level:", brcontrol.currB
        notification_controller.set_volume_bar( brcontrol.currB )
        notification_controller.show_notification()
        iter = 0
    else:
        iter += 1

def keyEvent_up(event):
    global sequence_held
    sequence_held.discard(event.Key)

############## attach to term ##############
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

def main(b_control, n_controller):
    global key_controls_bdown, key_controls_bup
    global notification_controller, brcontrol

    brcontrol = b_control

    with open(defaults) as key_maps:
        controls_json_root = json.load(key_maps)
        key_controls_bup = Set(controls_json_root['brightness-up'])
        key_controls_bdown = Set(controls_json_root['brightness-down'])

    # attach events to pyhook
    keyboard_hook_manager = pyxhook.HookManager()
    keyboard_hook_manager.KeyDown = keyEvent_down
    keyboard_hook_manager.KeyUp = keyEvent_up

    keyboard_hook_manager.HookKeyboard()
    keyboard_hook_manager.start()

    notification_controller = n_controller
    notification_controller.set_urgency(0)
    notification_controller.set_icon( notification_controller.ICON )

    try:
        while 1:
            time.sleep(0.1)
    except (KeyboardInterrupt, EOFError):
        keyboard_hook_manager.cancel()
        printError()
