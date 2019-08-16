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

"""mainwindow.py

Main application window. Coalesces all parts of the GUI and program logic.
Handles setting up most signal/slot connections, defining the program Actions
and so on.
"""

import platform

from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QMainWindow, QAction, QMessageBox

import freightplan.gui.iconmanager as IconManager
from freightplan import APP_NAME
from freightplan.planmanager import PlanManager
from freightplan.gui import Editor, Palette, Sidebar

class MainWindow(QMainWindow):
  """Main application window for freightplan.

  Bridges GUI and program logic and handles most signal/slot connections."""

  def __init__(self):
    """Constructor."""

    super().__init__()

    self.action = {}

    self.setWindowTitle(APP_NAME)
    self.resize(640, 480) # TEMP

    self.manager = PlanManager(self)
    self.manager.tabPane.currentChanged.connect(self.setActivePlan)
    self.setCentralWidget(self.manager.tabPane)

    self.sidebar = Sidebar(self)
    self.palette = Palette(self)
    self.palette.componentSelected.connect(self.manager.setCurrentEditorTileBrush)
    self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar)
    self.addDockWidget(Qt.RightDockWidgetArea, self.palette)

    self.statusbar = self.statusBar()

    self.create_actions()
    self.menubar = self.menuBar()
    self.create_menus()


  # TODO: Connect slots
  def create_actions(self):
    """Create the QActions used by the MainWindow."""

    self.action['new'] = QAction('&New Plan', self)
    self.action['new'].setShortcut(QKeySequence.New)
    self.action['new'].setStatusTip('Create a new plan')
    self.action['new'].triggered.connect(self.manager.newPlan)

    self.action['open'] = QAction('&Open Plan...', self)
    self.action['open'].setShortcut(QKeySequence.Open)
    self.action['open'].setStatusTip('Open an existing plan')
    self.action['open'].triggered.connect(self.manager.openPlan)

    self.action['reopen'] = QAction('&Reopen Closed Plan', self)
    self.action['reopen'].setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_T)
    self.action['reopen'].setStatusTip('Open the most recently closed plan')

    self.action['recent_clear'] = QAction('&Clear Recent Plans', self)
    self.action['recent_clear'].setStatusTip('Clear the recently opened plans '
                                             'list')

    self.action['close'] = QAction('&Close Plan', self)
    # Annoyingly, the QKeySequence.Close primary is Ctrl+F4 on Windows
    self.action['close'].setShortcut(Qt.CTRL + Qt.Key_W)
    self.action['close'].setStatusTip('Close the currently active plan')
    self.action['close'].triggered.connect(self.manager.closePlan)

    self.action['save'] = QAction('&Save Plan', self)
    self.action['save'].setShortcut(QKeySequence.Save)
    self.action['save'].setStatusTip('Save the currently active plan')
    self.action['save'].triggered.connect(self.manager.savePlan)

    self.action['save_as'] = QAction('Save Plan &As', self)
    self.action['save_as'].setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_S)
    self.action['save_as'].setStatusTip('Save the currently active plan under '
                                        'a different name')
    self.action['save_as'].triggered.connect(self.manager.savePlanAs)

    self.action['exit'] = QAction('E&xit', self)
    self.action['exit'].setShortcut(Qt.CTRL + Qt.Key_Q)
    self.action['exit'].setStatusTip(f'Exit {APP_NAME}')
    self.action['exit'].setMenuRole(QAction.MenuRole.QuitRole)
    self.action['exit'].triggered.connect(self.close)

    self.action['undo'] = QAction('&Undo', self)
    self.action['undo'].setShortcut(QKeySequence.Undo)

    self.action['redo'] = QAction('&Redo', self)
    self.action['redo'].setShortcut(QKeySequence.Redo)

    self.action['cut'] = QAction('Cu&t', self)
    self.action['cut'].setShortcut(QKeySequence.Cut)

    self.action['copy'] = QAction('&Copy', self)
    self.action['copy'].setShortcut(QKeySequence.Copy)

    self.action['paste'] = QAction('&Paste', self)
    self.action['paste'].setShortcut(QKeySequence.Paste)

    self.action['prefs'] = QAction('Pre&ferences', self)
    if platform.system() == 'Darwin':
      self.action['prefs'].setShortcut(QKeySequence.Preferences)
    else:
      self.action['prefs'].setShortcut(Qt.CTRL + Qt.Key_P)
    self.action['prefs'].setMenuRole(QAction.MenuRole.PreferencesRole)

    self.action['grid_show'] = QAction('Show &Grid', self)
    self.action['grid_show'].setCheckable(True)
    self.action['grid_show'].setChecked(True)
    self.action['grid_show'].setShortcut(Qt.CTRL + Qt.Key_G)
    self.action['grid_show'].setStatusTip('Toggle display of the editor grid')

    # TODO: Make a single-window About page with Qt info in a separate pane/tab
    # like other applications
    self.action['about'] = QAction('&About', self)
    self.action['about'].setMenuRole(QAction.MenuRole.AboutRole)
    self.action['about'].setStatusTip(f'Show information about {APP_NAME}')

    self.action['about_qt'] = QAction('About &Qt', self)
    self.action['about_qt'].setMenuRole(QAction.MenuRole.AboutQtRole)
    self.action['about_qt'].setStatusTip('Show information about the Qt library')
    self.action['about_qt'].triggered \
                           .connect(lambda x: QMessageBox.aboutQt(self))

  def create_menus(self):
    """Create the QMenus for the menubar."""

    menu_file = self.menubar.addMenu('&File')
    menu_file.addAction(self.action['new'])
    menu_file.addAction(self.action['open'])

    menu_recent = menu_file.addMenu('Open &Recent')
    menu_recent.addAction(self.action['reopen'])
    menu_recent.addSeparator()
    menu_recent.addAction('Recent plans not yet implemented') \
               .setDisabled(True) # TEMP
    menu_recent.addSeparator()
    menu_recent.addAction(self.action['recent_clear'])

    menu_file.addAction(self.action['close'])
    menu_file.addSeparator()
    menu_file.addAction(self.action['save'])
    menu_file.addAction(self.action['save_as'])
    menu_file.addSeparator()
    menu_file.addAction(self.action['exit'])

    menu_edit = self.menubar.addMenu('&Edit')
    menu_edit.addAction(self.action['undo'])
    menu_edit.addAction(self.action['redo'])
    menu_edit.addSeparator()
    menu_edit.addAction(self.action['cut'])
    menu_edit.addAction(self.action['copy'])
    menu_edit.addAction(self.action['paste'])

    menu_view = self.menubar.addMenu('&View')
    menu_view.addAction(self.action['grid_show'])

    menu_help = self.menubar.addMenu('&Help')
    menu_help.addAction(self.action['about'])
    menu_help.addAction(self.action['about_qt'])


  @Slot(int)
  def setActivePlan(self, tabIndex: int):
    """Sets the active plan; the plan that the Editor controls will affect.

    Handles reconnecting appropriate signals to the active Editor,
    synchronizing UI state, etc.

    Args:
      tabIndex: The index of the tab containing the plan to activate.
    """

    lastTab = self.manager.lastTab()
    gridShow = self.action['grid_show']
    if lastTab != -1:
      prevEditor = self.manager.editorAt(lastTab)
      gridShow.triggered.disconnect(prevEditor.grid.setVisible)
    if self.manager.tabPane.count():
      editor = self.manager.editorAt(tabIndex)
      gridShow.triggered.connect(editor.grid.setVisible)
      gridShow.setChecked(editor.grid.isVisible())
      self.palette.setEnabled(True)
    else:
      self.palette.setDisabled(True)


  # TODO: Do everything needed to close gracefully, e.g.
  #   - Prompt to save unsaved plans
  #   - anything else
  def closeEvent(self, event):
    """QWidget.closeEvent implementation."""
    return super().closeEvent(event)