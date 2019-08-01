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

"""document.py

Represents a document, which encapsulates a writable file and its metadata.
Such metadata includes file name, save path, last modification time, dirty
status and so on.
"""

from PySide2.QtCore import QDateTime, QFile, QFileInfo

class Document():
  """Document class. Encapsulate a writable file."""

  def __init__(self, fileName: str=None):
    """Constructor. Initializes a new document.

    Args:
      filename: The name of the file this document represents. Can be
                absolute or relative
    """

    self._fileinfo = QFileInfo(fileName)
    self._lastModifiedTime = QDateTime()
    self._lastSavedTime = QDateTime()


  def name(self) -> str:
    """Return the file name."""

    return self._fileinfo.baseName()


  def fileName(self) -> str:
    """Return the file name with extension."""

    return self._fileinfo.fileName()


  def absoluteFilePath(self) -> str:
    """Return the absolute path to the file."""

    return self._fileinfo.absoluteFilePath()


  def modified(self) -> bool:
    """Return whether the document has been modified since last write."""

    return not self._lastModifiedTime.isNull()


  def lastModified(self) -> int:
    """Return the time the document was modified without saving."""

    return self._lastModifiedTime.toSecsSinceEpoch()


  def lastSaved(self) -> int:
    """Return the time the document was saved."""

    return self._lastSavedTime.toSecsSinceEpoch()


  def save(self, fileName: str):
    """Saves the document to the filesystem.

    Raises an exception on failure.
    """

    pass


  def load(self, fileName: str):
    """Load a file from the filesystem into the document.

    Raises an exception on failure.
    """

    pass