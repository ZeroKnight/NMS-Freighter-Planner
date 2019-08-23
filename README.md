# NMS-Freighter-Planner

Freighter layout planning tool for Hello Games' No Man's Sky 🌌

## Notice

This program is currently under active early development; most things are
incomplete or missing entirely or the program could be in an entirely broken
state at any commit. As such, it is currently not entirely useful. That said,
check back every now and again as I work toward a useable alpha version!

## Build Instructions

If you're interested in poking around and what's currently here, there's a
couple required steps:

  * PySide2 (Qt for Python)
    * Can be installed via PIP: `pip install PySide2`
  * Compile the Qt Resource file. RCC should be bundled with PySide2 if
    acquired via `pip`.
    * `pyside2-rcc freightplan/resources.qrc -o freightplan/gui/resources_rc.py`
    * Eventually this won't be necessary.

Finally, simply run **main.py**.