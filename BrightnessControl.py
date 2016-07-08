import sys
import termios
import contextlib
import subprocess

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class BrightnessControl:
    def __init__(self):
        # get active monitor and current brightness
        self.monitor = self.getActiveMonitor()
        self.currB = self.getCurrentBrightness()

    def initStatus(self):
        if(self.monitor == "" or self.currB == ""):
            return False
        return True

    def getActiveMonitor(self):
        #Find display monitor
        monitor = subprocess.check_output("xrandr -q | grep ' connected' | cut -d ' ' -f1", shell=True)
        if(monitor != ""):
            monitor = monitor.split('\n')[0]
        return monitor

    def getCurrentBrightness(self):
        #Find current brightness
        currB = subprocess.check_output("xrandr --verbose | grep -i brightness | cut -f2 -d ' '", shell=True)
        if(currB != ""):
            currB = currB.split('\n')[0]
            currB = int(float(currB) * 100)
        else:
            currB = ""
        return currB

    def scale_moved(self, delta):
        #Change brightness
        self.currB = max(0, min(100, self.currB + delta))
        newBrightness = float(self.currB)/100
        cmd = "xrandr --output %s --brightness %.2f" % (self.monitor, newBrightness)
        cmdStatus = subprocess.check_output(cmd, shell=True)
