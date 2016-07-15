import platform
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ["./resources"]
includes = []
excludes = ["tkinter"]
packages = ["os", "json", "Xlib"]
build_exe_options = {"build_exe":"xBackLight","packages": packages, "excludes": excludes, "include_files": includefiles }


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if platform.system() == 'Windows':
    # base must be set on Windows to either console or gui app
    # testpubsub is currently a console application
    # base = 'Win32GUI'
    base = 'Console'
else:
    base = None

setup(  name = "xBackLight",
        version = "1.0",
        description = "xBackLight gives access to Linux OS brightness control using xrandr program mapped to key presses",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
