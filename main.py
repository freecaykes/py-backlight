from pybacklight import pybacklight, BrightnessControl
from gui_notification import xbacklight_notification_controller

def main():
    # new instance of BrightnessControl
    brcontrol = BrightnessControl()
    
    xnc = xbacklight_notification_controller()
    if(brcontrol.initStatus()):
        pybacklight.main(brcontrol, xnc)
    else:
        # error
        pybacklight.printError()
        sys.exit(1)

if __name__ == "__main__":
    main()
