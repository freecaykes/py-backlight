#!/usr/bin/env python

import sys
import termios
import contextlib
import subprocess
from sets import Set

class BrightnessControl:
    def __init__(self):
        # get active monitor and current brightness
        self.active_monitors = self.getActiveMonitor()
        self.currB = self.getCurrentBrightness()

    def initStatus(self):
        if(self.active_monitors == [] or self.currB == ""):
            return False
        return True

    def getActiveMonitor(self):
        #Find display monitor
        monitor = subprocess.check_output("xrandr -q | grep ' connected' | cut -d ' ' -f1", shell=True)
        if(monitor != ""):
            monitor = monitor.split('\n')

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

        cmd = ""
        for m in self.active_monitors:
            try:
                cmd = "xrandr --output %s --brightness %.2f" % (m, newBrightness)
                print cmd
                cmdStatus = subprocess.check_output(cmd, shell=True)
            except subprocess.CalledProcessError as e:
                # remove from active_monitors
                monitor_index = self.active_monitors.index( m )
                del self.active_monitors[ monitor_index ]
