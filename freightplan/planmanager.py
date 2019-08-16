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

"""planmanager.py

Manages open plans. Takes ownership of each Plan object created and
coordinates UI state with document/file state.
"""

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QTabWidget

import freightplan.components as Components
from freightplan.plan import Plan
from freightplan.gui import Editor, EditorView

TAB_HISTORY_SIZE = 5

class PlanManager(QObject):
  """Manages and coordinates Plans and their state with the UI state."""

  # Signals
  planCreated = Signal(Plan)
  planOpened = Signal(Plan)
  planClosing = Signal(Plan)
  planSaving = Signal(Plan)
  planSaved = Signal(Plan)

  def __init__(self, parent):
    """Constructor."""

    super().__init__(parent)

    self.parent = parent
    self.tabPane = QTabWidget(parent)
    self._tabHistory = [-1] * TAB_HISTORY_SIZE
    self._newPlanCount = 1

    self.tabPane.currentChanged.connect(self.handleLastTab)


  def currentEditor(self) -> Editor:
    """Return the Editor in the active tab."""

    currentIndex = self.tabPane.currentIndex()
    if currentIndex == -1:
      return None
    else:
      return self.tabPane.widget(currentIndex).editor()


  def viewAt(self, index) -> EditorView:
    """Return the EditorView in the tab at the specified index."""

    return self.tabPane.widget(index)


  def editorAt(self, index: int) -> Editor:
    """Return the Editor in the tab at the specified index."""

    return self.viewAt(index).editor()


  def handleLastTab(self, index: int):
    """Maintain a short history of previously active tabs."""

    self._tabHistory = [*self._tabHistory[1:], index]


  def lastTab(self) -> int:
    """Return the index of the last active tab."""

    try:
      return self._tabHistory[-2]
    except IndexError:
      return -1


  @Slot(Components.ComponentID)
  def setCurrentEditorTileBrush(self, cid: Components.ComponentID):
    """Set the tile brush for the current Editor."""

    currentEditor = self.currentEditor()
    if currentEditor:
      component = Components.componentByID(cid)
      currentEditor.setTileBrush(component.icon().pixmap(32, 32))


  @Slot()
  def newPlan(self):
    """Create a new Plan and add it to the manager.

    Typically called by the 'New' action.
    """

    # TODO: extension
    plan = Plan(f'New Plan {self._newPlanCount}')
    editor = Editor(plan, self)
    self._newPlanCount += 1
    index = self.tabPane.addTab(editor.view, plan.name())
    self.tabPane.setTabToolTip(index, plan.absoluteFilePath())
    self.planCreated.emit(plan)


  @Slot()
  def openPlan(self):
    """Open an existing Plan and add it to the manager."""

    filename = ''  # TODO: open file dialog

    if not filename:
      raise TypeError('filename cannot be empty or None')

    plan = Plan(filename)
    self.planOpened.emit(plan)


  @Slot()
  def savePlan(self):
    """Save the plan in the current tab."""

    index = self.tabPane.currentIndex()
    plan = self.editorAt(index).plan
    if not plan.modified():
      return

    self.planSaving.emit(plan)
    # do save stuff
    self.planSaved.emit(plan)


  @Slot()
  def savePlanAs(self):
    """Save the specified Plan as another file name."""

    index = self.tabPane.currentIndex()
    filename = ''  # TODO: save as dialog
    newPlan = Plan(filename)
    # copy plan data to newPlan
    # ensure newPlan.modified() returns true
    self.savePlan(newPlan)


  @Slot()
  def closePlan(self):
    """Close the Plan in the current tab and remove it from the manager."""

    index = self.tabPane.currentIndex()
    if index == -1:
      return

    plan = self.editorAt(index).plan
    self.planClosing.emit(plan)
    if plan.modified():
      # prompt to save
      pass

    self._tabHistory[-1] = -1
    self.tabPane.removeTab(index)