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

from freightplan.plan import Plan
from freightplan.gui import Editor

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
    self._plans = []
    self._newPlanCount = 1


  @Slot()
  def newPlan(self):
    """Create a new Plan and add it to the manager.

    Typically called by the 'New' action.
    """

    # TODO: extension
    plan = Plan(f'New Plan {self._newPlanCount}')
    editor = Editor(plan, self)
    self._newPlanCount += 1
    self._plans.append(plan)
    index = self.tabPane.addTab(editor.view, plan.name())
    self.tabPane.setTabToolTip(index, plan.absoluteFilePath())
    self.planCreated.emit(plan)


  @Slot(str)
  def openPlan(self, filename: str):
    """Open an existing Plan and add it to the manager.

    Args:
      filename: The name of the Plan to open.
    """

    if not filename:
      raise TypeError('filename cannot be empty or None')

    plan = Plan(filename)
    self._plans.append(plan)
    self.planOpened.emit(plan)


  @Slot(Plan)
  def savePlan(self, plan: Plan):
    """Save the specified Plan.

    Args:
      plan: The Plan to save.
    """

    if not plan.modified():
      return

    self.planSaving.emit(plan)
    # do save stuff
    self.planSaved.emit(plan)


  @Slot(Plan, str)
  def savePlanAs(self, plan: Plan, filename: str):
    """Save the specified Plan as the given file name.

    Args:
      plan: The Plan to save.
      filename: The name of the file to save the Plan as.
    """

    newPlan = Plan(filename)
    # copy plan data to newPlan
    # ensure newPlan.modified() returns true
    self.savePlan(newPlan)
    self._plans.remove(plan)
    self._plans.append(newPlan)


  @Slot(Plan)
  def closePlan(self, plan: Plan):
    """Close the specified Plan and remove it from the manager.

    Args:
      plan: The Plan to close.
    """

    self.planClosing.emit(plan)
    if plan.modified():
      # prompt to save
      pass

    self._plans.remove(plan)