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

import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets
from PySide2.QtCore import (
  Signal, Slot, QObject, QPoint, QPointF, QRectF, QSize, Qt
)
from PySide2.QtGui import QBrush, QPainter, QPen, QPixmap, QTransform
from PySide2.QtWidgets import (
  QGraphicsItem, QGraphicsObject, QGraphicsScene, QGraphicsView
)

from freightplan import GRID_SIZE
from freightplan.plan import Plan
from freightplan.gui.tile import Tile

cellSize = 32 # TEMP: keep this in Plan or something

# TEMP
import freightplan.gui.resources_rc

# TODO: slots for changing grid color, opacity, style, etc
class EditorGrid(QGraphicsObject):
  """A graphics object responsible for drawing the editor grid."""

  def __init__(self, parent: QGraphicsItem):
    """Constructor."""

    super().__init__(parent)

    self._color = Qt.gray
    self._style = Qt.SolidLine
    self._opacity = 1.0

    self._pen = QPen(self._color)
    self._pen.setStyle(self._style)

    self.setOpacity(self._opacity)


  @Slot(bool)
  def setVisible(self, visible):
    return super().setVisible(visible)


  def boundingRect(self):
    return self.parentItem().boundingRect()


  def paint(self, painter, option, widget):
    painter.setPen(self._pen)
    end = cellSize * GRID_SIZE
    for n in range(cellSize, end, cellSize):
      painter.drawLine(n, 0, n, end)
      painter.drawLine(0, n, end, n)


class EditorView(QGraphicsView):
  """QGraphicsView for Editor objects.

  Implements various zoom and scroll interactions, forwarding the rest to the
  Editor.
  """

  zoomChanged = Signal(float)

  def __init__(self, editor: 'Editor'):
    """Constructor.

    Args:
      editor: The Editor object to view.
    """

    super().__init__(editor)

    self._lastMousePos = QPoint()
    self._scaleFactors = [
      0.25, 0.33, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5
    ]
    self._currentScale = 1

    self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)


  def setZoom(self, factor: float):
    """Set the view's zoom scale to factor."""

    if factor == self._currentScale:
      return
    self._currentScale = factor
    self.zoomChanged.emit(factor)


  def zoomIn(self) -> bool:
    """Zoom the view in to the next increment.

    Returns whether or not the view is able to zoom further.
    """

    for factor in self._scaleFactors:
      if factor > self._currentScale:
        self.setZoom(factor)
        return True
    return False


  def zoomOut(self) -> bool:
    """Zoom the view out to the previous increment.

    Returns whether or not the view is able to zoom further.
    """

    for factor in reversed(self._scaleFactors):
      if factor < self._currentScale:
        self.setZoom(factor)
        return True
    return False


  def resetZoom(self):
    """Reset the view's zoom scale."""

    self.setZoom(1)


  def zoom(self):
    """Return the view's current zoom scale."""

    return self._currentScale


  def resizeEvent(self, event):
    """Implementation."""

    self.updateSceneRect(self._currentScale)


  def updateSceneRect(self, factor: float) -> QRectF:
    """Updates the associated scene's bounding rectangle.

    To make it possible to pan the view, the scene's bounding rectangle must
    be larger than the viewport. Scaling the view means that the scene in its
    entirety is scaled, including the scene's bounding rectangle, so it must
    be scaled along with the view.

    Currently, the view can be panned such that the editing grid can be
    freely moved around, but within the bounds of the viewport regardless of
    its size or zoom level, similar to Aseprite.

    Args:
      factor: The scaling factor the scene should be sized with respect to.

    Returns the updated scene bounding rectangle.
    """

    # TODO: make configurable via Property
    margin = QSize(10, 10) # Between edge of grid and viewport
    editAreaRect = self.scene().editArea.rect()
    editAreaSize = editAreaRect.size().toSize()

    # Make the scene 2x larger than the viewport, minus the editing grid. This
    # allows us to pan the grid up to the edges of the viewport (minus margin),
    # but no further. Also ensure the scene is at least big enough to encompass
    # the entire grid.
    sceneSize = self.maximumViewportSize() * 2 * (1 / factor)
    sceneSize = sceneSize - editAreaSize - margin
    sceneSize = sceneSize.expandedTo(editAreaSize + margin)
    newSceneRect = QRectF(QPointF(0,0), sceneSize)
    newSceneRect.moveCenter(editAreaRect.center())
    self.setSceneRect(newSceneRect)


  # TODO: Zoom widget on statusbar
  # TODO: See how much the delta is on horizontal wheel events and add support
  # for crazy mice like mine.
  # TODO: handle mice that report deltas finer than 120
  def wheelEvent(self, event: QtGui.QWheelEvent):
    """Implementation.

    Handles zooming the editor's view.
    """

    if (event.modifiers() & Qt.ControlModifier
        and event.orientation() == Qt.Vertical):
      if event.delta() > 0:
        self.zoomIn()
      else:
        self.zoomOut()

      # TODO: Improve cursor anchoring; be more like Aseprite
      prevAnchor = self.transformationAnchor()
      self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
      self.setTransform(QTransform.fromScale(self.zoom(), self.zoom()))
      self.updateSceneRect(self.zoom())
      self.setTransformationAnchor(prevAnchor)
      event.accept()
    else:
      super().wheelEvent(event)


  def mouseMoveEvent(self, event: QtGui.QMouseEvent):
    """Implementation.

    Handles panning the editor view.
    """

    if event.buttons() & Qt.MiddleButton:
      delta = self._lastMousePos - event.pos()
      hBar = self.horizontalScrollBar()
      vBar = self.verticalScrollBar()
      hBar.setValue(hBar.value() + delta.x())
      vBar.setValue(vBar.value() + delta.y())
      self._lastMousePos = event.pos()
    else:
      super().mouseMoveEvent(event)


  def mousePressEvent(self, event):
    """Implementation.

    Set up for panning. Remember this position for later and set the
    appropriate cursor.
    """

    if event.button() == Qt.MiddleButton:
      self._lastMousePos = event.pos()
      QtWidgets.QApplication.setOverrideCursor(Qt.ClosedHandCursor)
    else:
      super().mousePressEvent(event)


  def mouseReleaseEvent(self, event):
    """Implementation.

    Restore the mouse cursor if we're done panning.
    """

    if event.button() == Qt.MiddleButton:
      QtWidgets.QApplication.restoreOverrideCursor()
    else:
      super().mouseReleaseEvent(event)


class Editor(QGraphicsScene):
  """QGraphicsScene containing the editing area.

  Encapsulates a Plan, providing an interactive view to visualize and design
  the floor layout for the plan.
  """

  def __init__(self, plan: Plan, parent=None):
    """Constructor.

    Args:
      plan: The Plan to associate this Editor with.
      parent: The QObject that the Editor belongs to; typically a PlanManager.
    """

    super().__init__(parent)

    self.plan = plan
    self.lastTilePos = None
    self.view = EditorView(self)
    self.setBackgroundBrush(QBrush(Qt.lightGray))

    self.pix = QPixmap(':/images/corridor')

    length = cellSize * GRID_SIZE

    # Create border for grid area
    borderRect = QRectF(0, 0, length, length)
    pen = QPen(Qt.gray)
    brush = QBrush('#5e6787', Qt.SolidPattern)

    self.editArea = self.addRect(borderRect, pen, brush)
    self.grid = EditorGrid(self.editArea)
    self.view.centerOn(borderRect.center())


  def sceneToGrid(self, pos: QPointF) -> QPoint:
    """Map a scene position to grid coordinates."""

    return QPoint(pos.x() // cellSize, pos.y() // cellSize)


  # TODO: Handle things like selection areas and middle-click scrolling
  def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
    """Implementation.

    A left-click places a tile on a grid space, while a right-click removes a
    tile.
    """

    pos = event.buttonDownScenePos(event.button())
    item = self.itemAt(pos, QTransform())

    if event.button() is Qt.LeftButton:
      if not isinstance(item, Tile):
        coord = self.sceneToGrid(pos)
        t = Tile(self.pix, self.editArea)
        t.setPos(coord.x() * 32, coord.y() * 32)
        print(f'Placed tile at {coord!s}')
      else:
        event.ignore()
        return
    elif event.button() is Qt.RightButton:
      if isinstance(item, Tile):
        print(f'Removed tile at {self.sceneToGrid(pos)!s}')
        self.removeItem(item)
      else:
        event.ignore()
        return
    event.accept()


  def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
    """Implementation.

    Handles mouse movement events in the editor. Dragging the mouse with a
    button pressed will place or remove all tiles passed over.
    """

    pos = event.scenePos()
    tilePos = self.sceneToGrid(pos)
    item = self.itemAt(pos, QTransform())

    if tilePos != self.lastTilePos:
      self.lastTilePos = tilePos

      if event.buttons() & Qt.LeftButton:
        if not isinstance(item, Tile):
          t = Tile(self.pix, self.editArea)
          t.setPos(tilePos.x() * 32, tilePos.y() * 32)
          print(f'Placed tile at {tilePos!s}')
          # assert item is self.grid.cell(coord)
        else:
          event.ignore()
          return
      elif event.buttons() & Qt.RightButton:
        if isinstance(item, Tile):
          self.removeItem(item)
          print(f'Removed tile at {self.sceneToGrid(pos)!s}')
        else:
          event.ignore()
          return
    else:
      event.ignore()
    event.accept()