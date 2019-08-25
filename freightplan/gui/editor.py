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

"""editor.py

Defines classes for the interactive editing area. Editor is a subclass of a
QGraphicsScene that displays a grid space accepting placement of various
tiles representing freighter components such as corridors and rooms. Using
the EditorGrid class, visible grid lines can be drawn on the edit area to
aide positioning and placement. EditorView is a subclass of a QGraphicsView
that pairs with an Editor and displays it in the GUI.
"""

from typing import Union

import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets
from PySide2.QtCore import (
  Signal, Slot, QObject, QPoint, QPointF, QRectF, QSize, Qt
)
from PySide2.QtGui import QBrush, QPainter, QPen, QPixmap, QTransform
from PySide2.QtWidgets import (
  QGraphicsItem, QGraphicsObject, QGraphicsRectItem, QGraphicsScene,
  QGraphicsView
)

from freightplan import GRID_SIZE
from freightplan.plan import Plan
from freightplan.gui.tile import Tile

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
    self.setAcceptedMouseButtons(Qt.NoButton)


  @Slot(bool)
  def setVisible(self, visible):
    return super().setVisible(visible)


  def boundingRect(self):
    return self.parentItem().boundingRect()


  def paint(self, painter, option, widget):
    painter.setPen(self._pen)
    end = Plan.cellSize * GRID_SIZE
    for n in range(Plan.cellSize, end, Plan.cellSize):
      painter.drawLine(n, 0, n, end)
      painter.drawLine(0, n, end, n)


class EditorView(QGraphicsView):
  """QGraphicsView for Editor objects.

  Implements various zoom and scroll interactions, forwarding the rest to the
  Editor.
  """

  editor = QGraphicsView.scene  # Friendly alias

  panStarted = Signal(QPointF)
  panEnded = Signal(QPointF)
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

    self.setMouseTracking(True)
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
    editAreaRect = self.editor().editArea.rect()
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

    return newSceneRect


  # TODO: Zoom widget on statusbar
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
    elif event.orientation() == Qt.Horizontal:
      # XXX: Workaround for the insane horizontal scroll delta of 15240 on the
      # Logitech G502 mouse.
      if abs(event.delta()) == 15240:
        newDelta = 120 if event.delta() > 0 else -120
        event = QtGui.QWheelEvent(
          event.pos(), event.globalPos(), newDelta, event.buttons(),
          event.modifiers(), orient=Qt.Horizontal
        )
      super().wheelEvent(event)
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

    super().mouseMoveEvent(event)


  def mousePressEvent(self, event):
    """Implementation.

    Set up for panning. Remember this position for later and set the
    appropriate cursor.
    """

    pos = event.pos()
    if event.button() == Qt.MiddleButton:
      self._lastMousePos = pos
      self.panStarted.emit(self.mapToScene(pos))
      QtWidgets.QApplication.setOverrideCursor(Qt.ClosedHandCursor)

    super().mousePressEvent(event)


  def mouseReleaseEvent(self, event):
    """Implementation.

    Restore the mouse cursor if we're done panning.
    """

    pos = event.pos()
    if event.button() == Qt.MiddleButton:
      QtWidgets.QApplication.restoreOverrideCursor()
      self.panEnded.emit(self.mapToScene(pos))

    super().mouseReleaseEvent(event)


class EditArea(QGraphicsRectItem):
  """QGraphicsRectItem representing the editing area."""

  def __init__(self, rect: QRectF, editor: 'Editor'):
    """Constructor."""

    super().__init__(rect)

    self.editor = editor
    self._hoveredCell = None
    self.lastTilePos = None

    self.setPen(QPen(Qt.gray))
    self.setBrush(QBrush('#5e6787', Qt.SolidPattern))
    self.setAcceptHoverEvents(True)
    self.editor.addItem(self)


  @Slot()
  def unsetHoveredCell(self):
    """Unsets the currently hovered cell."""

    self._hoveredCell = None
    self.update()


  @Slot(QPointF)
  def setHoveredCell(self, pos: Union[QPoint, QPointF]):
    """Sets the currently hovered cell.

    Args:
      pos: If given as a QPoint, specifies the position of the cell in grid
           coordinates. If given as a QPointF, specifies the position of the
           cell in scene coordinates.
    """

    if isinstance(pos, QPointF):
      pos = Editor.sceneToGrid(pos)

    if Editor.validGridPos(pos):
      self._hoveredCell = pos
    else:
      raise ValueError('Cannot set hovered cell to invalid position ({}, {})'
                       .format(pos.x(), pos.y()))
    self.update()


  def paint(self, painter, option, widget):
    """Implementation.

    Handle drawing "ghost" tiles when hovering over grid cells.
    """

    super().paint(painter, option, widget)
    pixmap = self.editor._tileBrush
    if self._hoveredCell and pixmap:
      scenePos = Editor.gridToScene(self._hoveredCell)
      fragment = QPainter.PixmapFragment.create(
        scenePos + QPointF(pixmap.width() / 2, pixmap.height() / 2),
        QRectF(QPointF(0, 0), pixmap.size()),
        rotation=self.editor._tileRotation,
        opacity=0.75
      )
      painter.drawPixmapFragments(fragment, 1, pixmap)


  def hoverMoveEvent(self, event):
    """Implementation.

    Keeps track of the cell the cursor is hovering over for other events to
    make use of.
    """

    pos = Editor.sceneToGrid(event.pos())
    if Editor.validGridPos(pos):
      if pos != self.lastTilePos:
        self.lastTilePos = pos
        self.setHoveredCell(pos)
    else:
      self.unsetHoveredCell()


  def hoverLeaveEvent(self, event):
    """Implementation."""

    self.unsetHoveredCell()


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

    self._tileBrush = None
    self._tileRotation = 0
    self._currentFloor = 0

    length = Plan.cellSize * GRID_SIZE

    # Create editing area
    borderRect = QRectF(0, 0, length, length)
    self.editArea = EditArea(borderRect, self)
    self.grid = EditorGrid(self.editArea)
    self.view.centerOn(borderRect.center())

    self.view.panStarted.connect(self.editArea.unsetHoveredCell)
    self.view.panEnded.connect(self.editArea.setHoveredCell)


  @staticmethod
  def sceneToGrid(pos: QPointF) -> QPoint:
    """Map a scene position to grid coordinates."""

    return QPoint(pos.x() // Plan.cellSize, pos.y() // Plan.cellSize)


  @staticmethod
  def gridToScene(pos: QPoint) -> QPointF:
    """Map grid coordinates to a scene position."""

    return QPointF(pos.x() * Plan.cellSize, pos.y() * Plan.cellSize)

  @staticmethod
  def validGridPos(pos: Union[QPointF, QPoint], scene: bool=False) -> bool:
    """Return whether the given scene position is within the grid.

    Args:
      pos: The position to validate. Can be either a QPointF or QPoint.
      scene: If true, pos represents a scene coordinate, otherwise pos is a
             grid coordinate. Defaults to false, i.e. a grid coordinate.
    """

    coord = __class__.sceneToGrid(pos) if scene else pos
    return 0 <= coord.x() < GRID_SIZE and 0 <= coord.y() < GRID_SIZE

  def setTileBrush(self, pixmap: QPixmap):
    """Set the tile to be placed when painting on the Editor.

    Args:
      pixmap: The tile pixmap to set the brush to.
    """

    self._tileBrush = pixmap
    self._tileRotation = 0


  def currentFloor(self) -> 'Floor':
    """Return the currently active Floor object."""

    return self.plan.floorAt(self._currentFloor)


  def itemAtGridPos(self, pos: QPoint, transform: QTransform) -> QGraphicsItem:
    """Return the QGraphicsItem at the specified grid coordinate.

    Functions similarly to the base itemAt() method."""

    # Adjust the position to the center of the grid cell to ensure the item is
    # under the cursor. Items with even dimensions have a sub-pixel center,
    # causing it to be shifted one pixel when rotating.
    center = Plan.cellSize / 2
    scenePos = self.gridToScene(pos) + QPointF(center, center)

    return self.itemAt(scenePos, transform)


  def placeTile(self, tile: Tile, pos: QPoint):
    """Place a tile on the Editor.

    Args:
      tile: The tile to place.
      pos: The position in grid coordinates to place the tile, given as a
           QPoint.
    """

    if self.validGridPos(pos):
      self.currentFloor().cellAt(pos).setTile(tile)
      tile.setVisible(True)
      tile.setRotation(self._tileRotation)
      scenePos = self.gridToScene(pos)
      tile.setPos(scenePos)
      print(f'Placed tile at {pos!s}')
    else:
      raise ValueError(f'Grid position out of bounds: {pos.x()}, {pos.y()}')


  def removeTile(self, pos: QPoint):
    """Remove a tile from the Editor.

    Args:
      pos: The position in grid coordinates to place the tile, given as a
           QPoint.
    """

    if self.validGridPos(pos):
      cell = self.currentFloor().cellAt(pos)
      self.removeItem(cell.tile())
      cell.clearTile()
      print(f'Removed tile at {pos!s}')
    else:
      raise ValueError(f'Grid position out of bounds: {pos.x()}, {pos.y()}')


  def handleLeftButton(self, pos: QPointF):
    """Handles the left mouse button for the Editor area."""

    coord = self.sceneToGrid(pos)
    item = self.itemAtGridPos(coord, QTransform())
    if isinstance(item, Tile):
      # TODO: Handle different rotations
      if item.pixmap().cacheKey() != self._tileBrush.cacheKey():
        self.removeTile(coord)
      else:
        return
    self.placeTile(Tile(self._tileBrush, self.editArea), coord)


  def handleRightButton(self, pos: QPointF):
    """Handles the right mouse button for the Editor area."""

    coord = self.sceneToGrid(pos)
    item = self.itemAtGridPos(coord, QTransform())
    if isinstance(item, Tile):
      self.removeTile(coord)


  # TODO: Handle things like selection areas and middle-click scrolling
  def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
    """Implementation.

    A left-click places a tile on a grid space, while a right-click removes a
    tile.
    """

    pos = event.buttonDownScenePos(event.button())
    if self.validGridPos(pos, scene=True):
      self.lastTilePos = self.sceneToGrid(pos)
      if event.button() is Qt.LeftButton:
        self.handleLeftButton(pos)
      elif event.button() is Qt.RightButton:
        self.handleRightButton(pos)

    super().mouseMoveEvent(event)


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
      if self.validGridPos(tilePos):
        if event.buttons() & Qt.LeftButton:
          self.handleLeftButton(pos)
        elif event.buttons() & Qt.RightButton:
          self.handleRightButton(pos)

    super().mouseMoveEvent(event)


  def keyPressEvent(self, event):
    """Implementation."""

    if event.key() == Qt.Key_R:
      if event.modifiers() & Qt.ShiftModifier:
        self._tileRotation -= 90
      else:
        self._tileRotation += 90
      self._tileRotation %= 360
      self.editArea.update()

    super().keyPressEvent(event)