import platform
from distutils.core import setup

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ["./resources"]


setup(  name = "xBackLight",
        version = "1.0",
        packages = ['pybacklight','gui_notification' ],
        description = "xBackLight gives access to Linux OS brightness control using xrandr program mapped to key presses",
        author='freecaykes',
        url='https://github.com/freecaykes/pybacklight',
        platforms="Gnome",
        license="MIT License",
        classifiers= [
            'Development Status :: 1 - Alpha',
        ],
        install_requires = [
            'python-xlib'
        ]
    )
