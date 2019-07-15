# This file is part of freightplan - No Man's Sky Freighter Planner
# Copyright (C) 2019  Alex "ZeroKnight" George
#
# freightplan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# freightplan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# TODO: docstring

# import stuff from gui and other program modules
from PySide2.QtWidgets import QApplication

from freightplan.gui.mainwindow import MainWindow

# initialize and set up the gui; provide entry to gui main loop
# this will be what main.py calls to do the actual work

class App(QApplication):
  def __init__(self, args):
    super().__init__(args)

    self.window = MainWindow()
    self.window.show()