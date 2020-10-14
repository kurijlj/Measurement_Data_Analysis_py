
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
# 2020-10-14 Ljubomir Kurij <kurijlj@gmail.com>
#
# * datasets_unit_tsesting.py: created.
#
# =============================================================================


# ============================================================================
#
# TODO:
#
#
# ============================================================================


# ============================================================================
#
# References (this section should be deleted in the release version)
#
#
# ============================================================================

# =============================================================================
# Modules import section
# =============================================================================

import unittest
import datasets
from PySide2.QtCore import (
    QAbstractItemModel,
    Qt
    )
from PySide2.QtGui import (
    QColor,
    QPen
    )


# =============================================================================
# Test cases
# =============================================================================

TEST_CASES = [
    # Empty dataset (uninitialized).
    datasets.EmptyDataset(),
    ]


# =============================================================================
# Unit testing classes
# =============================================================================

class TestEmptyDataset(unittest.TestCase):
    """TODO: Put class docstring HERE.
    """

    def setUp(self):
        """TODO: Put method docstring HERE.
        """

        self._dataset = TEST_CASES[0]

    def testPropertyX(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.x, None)

    def testChangePlotStatusIndexError(self):
        """TODO: Put method docstring HERE.
        """

        with self.assertRaises(IndexError):
            self._dataset.changePlotStatus(-1)
        with self.assertRaises(IndexError):
            self._dataset.changePlotStatus(1)

    @unittest.expectedFailure
    def testChangePlotStatusIndexErrorFail(self):
        """TODO: Put method docstring HERE.
        """

        with self.assertRaises(IndexError):
            self._dataset.changePlotStatus(0)

    def testColumnCount(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.columnCount(), 1)

    def testDataIndexErrorFail(self):
        """TODO: Put method docstring HERE.
        """

        index1 = self._dataset.createIndex(-1, 0)
        index2 = self._dataset.createIndex(1, 0)

        with self.assertRaises(IndexError):
            self._dataset.data(index1)

        with self.assertRaises(IndexError):
            self._dataset.data(index2)

    def testData(self):
        """TODO: Put method docstring HERE.
        """

        index = self._dataset.createIndex(0, 0)

        self.assertEqual(self._dataset.data(index), 'None')
        self.assertEqual(self._dataset.data(index, Qt.DisplayRole), 'None')
        self.assertEqual(
            self._dataset.data(index, Qt.BackgroundRole),
            QColor(Qt.white)
            )
        self.assertEqual(
            self._dataset.data(index, Qt.TextAlignmentRole),
            Qt.AlignRight
            )
        self.assertEqual(self._dataset.data(index, Qt.UserRole), None)
        self.assertEqual(self._dataset.data(index, None), None)

    def testDisplayPrecisionString(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.displayPrecisionString(0), None)

    def testGetDrawingPen(self):
        """TODO: Put method docstring HERE.
        """

        pen = QPen(
            QColor(Qt.white),
            0.5,
            Qt.SolidLine,
            Qt.RoundCap,
            Qt.RoundJoin
            )

        self.assertEqual(self._dataset.getDrawingPen(0), pen)

    def testHeaderData(self):
        """TODO: Put method docstring HERE.
        """

        role = Qt.DisplayRole
        orientation = Qt.Horizontal

        self.assertEqual(self._dataset.headerData(0, None, None), None)
        self.assertEqual(self._dataset.headerData(0, None, role), '0')
        self.assertEqual(
            self._dataset.headerData(0, orientation, role),
            'None'
            )

    def testIsEmptyDataset(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.isEmptyDataset(), True)

    def testRowCount(self):
        """TODO: Put method docstring HERE.
        """

        self.assertEqual(self._dataset.rowCount(), 1)

    @unittest.expectedFailure
    def testSetDisplayPrecision(self):
        """TODO: Put method docstring HERE.
        """

        with self.assertRaises(IndexError):
            self._dataset.setDisplayPrecision(0, 10)

    @unittest.expectedFailure
    def testSetX(self):
        """TODO: Put method docstring HERE.
        """

        with self.assertRaises(IndexError):
            self._dataset.setDisplayPrecision(0)


# =============================================================================
# Script main body
# =============================================================================

if __name__ == '__main__':
    unittest.main()
