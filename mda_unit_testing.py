
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
# 2020-09-19 Ljubomir Kurij <kurijlj@gmail.com>
#
# * mda.py: created.
#
# =============================================================================


# ============================================================================
#
# TODO:
#
# * Add separate method to DataViewWidget for initializing chart axes.
#
# * Implement type checking using Mypy.
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

import models
import unittest
import numpy as np


# =============================================================================
# Test cases
# =============================================================================

class TestCustomTableModel(unittest.TestCase):
    """TODO: Put class docstring HERE.
    """

    test_cases = [
        # Uninitialized.
        models.DataSet(None, None),
        # Empty headers and data.
        models.DataSet((None), (None)),
        # Initialization with valid data set (2D data table).
        models.DataSet(
            ['C1', 'C2', 'C3'],
            np.array((1, 2, 3, 4, 5, 6, 7, 8, 9)).reshape((3, 3))
            ),
        # Headers with one None section and tuple instead of ndarray as the
        # data set.
        models.DataSet(
            ['C1', None, 'C3'],
            (1, 2, 3, 4, 5, 6, 7, 8, 9)
            ),
        # Headers sections count and column count doesn't coincide.
        models.DataSet(
            ['C1', 'C3'],
            np.array((1, 2, 3, 4, 5, 6, 7, 8, 9)).reshape((3, 3))
            ),
        # Initialization with invalid data types (int, int).
        models.DataSet(54, 23),
        # Initialization with invalid data types (string, int).
        models.DataSet('Hello', 23),
        # Initialization with invalid data types (int, string).
        models.DataSet(54, 'Hello'),
        # Initialization with invalid data types (string, string).
        models.DataSet('Hello', 'Hello'),
        # Initialization with valid data set (1D data table).
        models.DataSet(
            ['C1'],
            np.array((1, 2, 3, 4, 5, 6, 7, 8, 9))
            ),
        # Initialization with valid data set (2D data table).
        models.DataSet(
            ['C1', 'C2'],
            np.array((1, 2, 3, 4, 5, 6)).reshape((3, 2))
            ),
        # Initialization with valid data set (2D data table), except one
        # headers section is set to None.
        models.DataSet(
            ['C1', None, 'C3'],
            np.array((1, 2, 3, 4, 5, 6, 7, 8, 9)).reshape((3, 3))
            ),
        ]

    @unittest.expectedFailure
    def initialization_type_check_valid(self):
        """Method to test initialization type checking facility for the
        CustomTableModel class, when object is initialized with valid,
        data sets, i.e. the ones that class knows how to handle.
        """

        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_cases[0])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_cases[1])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_cases[2])

    def initialization_type_check_invalid(self):
        """Method to test initialization type checking facility for the
        CustomTableModel class, when object is initialized with invalid,
        data sets.
        """

        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_cases[3])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_cases[5])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_cases[6])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_cases[7])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_cases[8])

    @unittest.expectedFailure
    def initialization_coincidence_check_valid(self):
        """Method to test facility for verification of headers sections number
        and columns number coincidence during objects initialization, when
        object is initialized with valid data sets.
        """

        with self.assertRaises(ValueError):
            models.CustomTableModel(TestCustomTableModel.test_cases[0])
        with self.assertRaises(ValueError):
            models.CustomTableModel(TestCustomTableModel.test_cases[1])
        with self.assertRaises(ValueError):
            models.CustomTableModel(TestCustomTableModel.test_cases[2])
        with self.assertRaises(ValueError):
            models.CustomTableModel(TestCustomTableModel.test_cases[3])

    def initialization_coincidence_check_invalid(self):
        """Method to test facility for verification of headers sections number
        and columns number coincidence during objects initialization, when
        object is initialized with invalid data sets.
        """

        with self.assertRaises(ValueError):
            models.CustomTableModel(TestCustomTableModel.test_cases[4])

    def test_row_count_method(self):
        """Method to test rowCount facility of the CustomTableModel class.
        """

        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[0])
        self.assertEqual(mdl.rowCount(), 1)
        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[1])
        self.assertEqual(mdl.rowCount(), 1)
        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[2])
        self.assertEqual(mdl.rowCount(), 3)
        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[9])
        self.assertEqual(mdl.rowCount(), 9)
        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[10])
        self.assertEqual(mdl.rowCount(), 3)

    def test_column_count_method(self):
        """Method to test columnCount facility of the CustomTableModel class.
        """

        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[0])
        self.assertEqual(mdl.columnCount(), 1)
        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[1])
        self.assertEqual(mdl.columnCount(), 1)
        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[2])
        self.assertEqual(mdl.columnCount(), 3)
        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[9])
        self.assertEqual(mdl.columnCount(), 1)
        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[10])
        self.assertEqual(mdl.columnCount(), 2)

    def test_header_string_method(self):
        """Method to test _headerString facility of the CustomTableModel class.
        """

        mdl = models.CustomTableModel(TestCustomTableModel.test_cases[0])
        self.assertEqual(mdl._headerString(3), '3 [x]')


# =============================================================================
# Script main body
# =============================================================================

if __name__ == '__main__':
    unittest.main()
