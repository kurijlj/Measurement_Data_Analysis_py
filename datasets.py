
#!/usr/bin/env python3
"""TODO: Put module docstring HERE.
"""

# =============================================================================
# Copyright (C) 2020 Ljubomir Kurij <kurijlj@gmail.com>
#
# This file is part of mda (Measurement Data Analytics).
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option)
# any later version.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =============================================================================


# =============================================================================
#
# This program uses code from Qt for Python examples of the Qt Toolkit
# <https://doc.qt.io/qtforpython/_downloads/06ada84b04e72c9468651471cc91b026/
# datavisualize.tar.bz2> by The Qt Company Ltd., available under a
# 3-Clause BSD License.
#
# 2020-10-13 Ljubomir Kurij <kurijlj@gmail.com>
#
# * dataset.py: created.
#
# =============================================================================


# ============================================================================
#
# TODO:
#
# * Implement distinct model classes for handling different cases of dataset
#   initialization: empty dataset, no data (just headers), one column dataset,
#   data table. Since we are using read csv facility from pandas module,
#   loading data without headers is not possible (this is only possible if
#   dataset is empty.
#
# ============================================================================


# ============================================================================
#
# References (this section should be deleted in the release version)
#
# * For implementing abstract base classes take a look at the abc module, and:
#       1) https://docs.python.org/3/library/abc.html
#       2) https://www.python-course.eu/python3_abstract_classes.php
#       3) https://medium.com/@s.martinallo/abstract-virtual-classes-with-python-48bf60d00d9e
#       4) https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_prototype.htm
#
# ============================================================================

# =============================================================================
# Modules import section
# =============================================================================

from PySide2.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt
    )
from PySide2.QtGui import (
    QColor,
    QPen
    )


# =============================================================================
# Module level constants
# =============================================================================


# =============================================================================
# Datasets classes and functions
# =============================================================================

class DatasetTableModel(QAbstractTableModel):
    """TODO: Put class docstring here.
    """

    def __init__(self):
        super().__init__()

    def _checkColumnIndex(self, column):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def _checkRowIndex(self, row):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def _headerString(self, column):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    @property
    def x(self):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def changePlotStatus(self, column, plot=False):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def checkPlotStatus(self, column):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def columnCount(self, parent=QModelIndex):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def data(self, index, role=Qt.DisplayRole):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def displayPrecisionString(self, column):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def getDrawingPen(self, column):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def headerData(self, section, orientation, role):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def isEmptyDataset(self):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def rowCount(self, parent=QModelIndex):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def setDisplayPrecision(self, column, precision):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')

    def setX(self, new):
        """TODO: Put method docstring here.
        """

        raise NotImplementedError('Override method in the derived class')


class EmptyDataset(QAbstractTableModel):
    """TODO: Put class docstring here.
    """

    def __init__(self):
        super().__init__()

    def _checkColumnIndex(self, column):
        """TODO: Put method docstring here.
        """

        if column != 0:
            raise IndexError('column index out of range')

    def _checkRowIndex(self, row):
        """TODO: Put method docstring here.
        """

        if row != 0:
            raise IndexError('row index out of range')

    def _headerString(self, section, orientation):
        """TODO: Put method docstring here.
        """

        self._checkColumnIndex(section)

        if orientation == Qt.Horizontal:
            return 'None'

        return '0'

    @property
    def x(self):
        """TODO: Put method docstring here.
        """

        return None

    def changePlotStatus(self, column, plot=False):
        """TODO: Put method docstring here.
        """

        self._checkColumnIndex(column)

    def checkPlotStatus(self, column):
        """TODO: Put method docstring here.
        """

        self._checkColumnIndex(column)

        return False

    def columnCount(self, parent=QModelIndex):
        """TODO: Put method docstring here.
        """

        return 1

    def data(self, index, role=Qt.DisplayRole):
        """TODO: Put method docstring here.
        """

        row = index.row()
        column = index.column()

        self._checkRowIndex(row)
        self._checkColumnIndex(column)

        if role == Qt.DisplayRole:
            return 'None'

        if role == Qt.BackgroundRole:
            return QColor(Qt.white)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        if role == Qt.UserRole:
            pass

        return None

    def displayPrecisionString(self, column):
        """TODO: Put method docstring here.
        """

        self._checkColumnIndex(column)

        return None

    def getDrawingPen(self, column):
        """TODO: Put method docstring here.
        """

        self._checkColumnIndex(column)

        pen = QPen(
            QColor(Qt.white),
            0.5,
            Qt.SolidLine,
            Qt.RoundCap,
            Qt.RoundJoin
            )

        return pen

    def headerData(self, section, orientation, role):
        """TODO: Put method docstring here.
        """

        if role != Qt.DisplayRole:
            return None

        return self._headerString(section, orientation)

    def isEmptyDataset(self):
        """TODO: Put method docstring here.
        """

        return True

    def rowCount(self, parent=QModelIndex):
        """TODO: Put method docstring here.
        """

        return 1

    def setDisplayPrecision(self, column, precision):
        """TODO: Put method docstring here.
        """

        self._checkColumnIndex(column)

    def setX(self, new):
        """TODO: Put method docstring here.
        """

        self._checkColumnIndex(new)
