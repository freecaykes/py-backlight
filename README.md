# py-backlight

xBackLight gives access to Linux OS brightness control using xrandr program mapped to key presses

## Prerequisites

- python-xlib 1.4
- x11 (xandr)
- cx_Freeze (build)

## Installation

Install by running the INSTALL.sh to add as a startup program

or to build the binary

```
python setup.py build
```

## Key Controls

Configure the brightness-up command and brightness-down command with a combination of key commands in **resources/keymap.json**.  The listed keys in the JSON array must be simultanerously pressed for the action to take place.
