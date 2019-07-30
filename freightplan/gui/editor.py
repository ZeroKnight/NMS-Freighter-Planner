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

from PySide2.QtCore import QMarginsF, QPoint, QPointF, QRectF, Qt
from PySide2.QtGui import QBrush, QPainter, QPen, QPixmap, QTransform
import PySide2.QtWidgets as QtWidgets
from PySide2.QtWidgets import (
  QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
)

from freightplan import GRID_SIZE

# TEMP
import freightplan.gui.resources_rc

class Tile(QGraphicsPixmapItem):
  """Represents a placed component on the Editor grid.

  Consists of a pixmap item whose parent is the grid cell QRect it was placed
  in. Its bounding rectangle is set to match the parent grid cell.
  """

  def __init__(self, pixmap: QPixmap, parent: QtWidgets.QGraphicsRectItem):
    """Constructor.

    Initializes a QGraphicsPixmapItem and set its positon to its parent.

    Args:
      pixmap: The QPixmap to display for the tile.
      parent: The QGraphicsRectItem that this tile is a child of.
    """

    super().__init__(pixmap, parent)

    # Ensure the shape consists of the whole pixmap and not just the opaque
    # portion, otherwise the background rect would be selected.
    self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)

    self.setPos(self.parentItem().rect().topLeft())


class EditorGrid():
  """Data structure of the grid represented by the Editor class.

  The grid is implemented as a two-dimensional list whose indices are the (x,y)
  position of a grid cell and whose values are dicts with the following keys:
    - cell: The underlying QGraphicsRectItem that represents the grid cell
    - tile: The Tile that was placed
  """

  def __init__(self, editor):
    """Constructor.

    Initialize the grid with GRID_SIZE rows and columns.

    Args:
      editor: The Editor instance that this grid belongs to
    """

    self._grid = [
      [
        {'cell': None, 'tile': None} for y in range(GRID_SIZE)
      ] for x in range(GRID_SIZE)
    ]
    self.editor = editor


  def cell(self, pos: QPoint) -> QGraphicsRectItem:
    """Return the cell at the given position."""

    return self._grid[pos.x()][pos.y()].get('cell')


  def tile(self, pos: QPoint) -> Tile:
    """Return the Tile at the given position, or None if there isn't one."""

    return self._grid[pos.x()][pos.y()].get('tile', None)


  def set_cell(self, pos: QPoint, cell: QGraphicsRectItem):
    """Set the cell at the given position to cell."""

    self._grid[pos.x()][pos.y()]['cell'] = cell


  def set_tile(self, pos: QPoint, tile: Tile):
    """Set the Tile at the given position to tile."""

    self._grid[pos.x()][pos.y()]['tile'] = tile


class Editor(QGraphicsScene):
  """QGraphicsScene containing the editing area.

  Defines the grid-space representing the floor layout of the freighter.
  """

  def __init__(self, parent):
    """Constructor.

    Args:
      parent: The widget that the Editor belongs to. Usually a MainWindow.
    """

    super().__init__(parent)

    # TBD: EditorView class?
    self.view = QGraphicsView(self)
    # TODO: implement drag on middle-mouse or maybe ctrl-click. Depends on
    # other user interactions
    # self.view.setDragMode(QGraphicsView.ScrollHandDrag)

    self._cell_size = 32 # px
    self.grid = EditorGrid(self)
    self.pix = QPixmap(':/images/corridor')

    self._init_grid()


  def _init_grid(self):
    """Create the grid for the Editor."""

    length = self._cell_size * GRID_SIZE

    border_rect = QRectF(0, 0, length, length)
    pen = QPen(Qt.gray)
    brush = QBrush('#5e6787', Qt.SolidPattern)
    grid_border = self.addRect(border_rect, pen, brush)
    self.setSceneRect(border_rect.marginsAdded(QMarginsF(5, 5, 5, 5)))

    for x in range(GRID_SIZE):
      for y in range(GRID_SIZE):
        cs = self._cell_size
        rect = QRectF(x * cs, y * cs, cs, cs)
        item = self.addRect(rect, pen)
        item.setParentItem(grid_border)
        self.grid.set_cell(QPoint(x, y), item)


  def get_grid_pos(self, cell: QGraphicsRectItem) -> QPoint:
    """Get position of grid cell in grid coordinates as a QPoint."""

    rect = cell.rect()
    return QPoint(cell.mapToScene(rect.topLeft()).toPoint() / self._cell_size)


  def scene_to_grid(self, pos: QPointF) -> QPoint:
    """Map a scene position to grid coordinates."""

    cs = self._cell_size
    return QPoint(int(pos.x()) / cs, int(pos.y()) / cs)


  # TODO: Bound minimum zoom to fit the View area
  # TODO: create a proper view class and forward sceneevents to it
  def wheelEvent(self, event: QtWidgets.QGraphicsSceneWheelEvent):
    """Implementation.

    Handles zooming the editor's view.
    """

    zoom_factor = 1.15

    if event.modifiers() & Qt.ControlModifier:
      if event.delta() > 0:
        self.view.scale(zoom_factor, zoom_factor)
      else:
        self.view.scale(1 / zoom_factor, 1 / zoom_factor)
      event.accept()
    else:
      event.ignore()


  def mousePressEvent(self, event):
    """Implementation.

    Handles mouse-presses in the editor. A left-click places a tile on a grid
    space, while a right-click removes a tile.
    """

    pos = event.buttonDownScenePos(event.button())
    item = self.itemAt(pos, QTransform())

    if not item:
      event.ignore()
      return

    if event.button() is Qt.LeftButton:
      if isinstance(item, QGraphicsRectItem):
        coord = self.get_grid_pos(item)
        self.grid.set_tile(coord, Tile(self.pix, item))
        print(f'Placed tile at {coord!s}')
        assert item is self.grid.cell(coord)
      else:
        event.ignore()
        return
    elif event.button() is Qt.RightButton:
      if isinstance(item, Tile):
        print(f'Removed tile at {self.scene_to_grid(pos)!s}')
        self.removeItem(item)
      else:
        event.ignore()
        return
    event.accept()


# TODO: Drag event for placing tiles continuously