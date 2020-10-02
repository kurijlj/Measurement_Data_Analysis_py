
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
    test_data_sets = [
        models.DataSet(None, None),
        models.DataSet((None), (None)),
        models.DataSet(
            ['C1', 'C2', 'C3'],
            np.array((1, 2, 3, 4, 5, 6, 7, 8, 9)).reshape((3, 3))
            ),
        models.DataSet(
            ['C1', None, 'C3'],
            (1, 2, 3, 4, 5, 6, 7, 8, 9)
            ),
        models.DataSet(
            ['C1', 'C3'],
            np.array((1, 2, 3, 4, 5, 6, 7, 8, 9)).reshape((3, 3))
            ),
        models.DataSet(54, 23),
        models.DataSet('Hello', 23),
        models.DataSet(54, 'Hello'),
        models.DataSet('Hello', 'Hello'),
        models.DataSet(
            ['C1'],
            np.array((1, 2, 3, 4, 5, 6, 7, 8, 9))
            ),
        models.DataSet(
            ['C1', 'C2'],
            np.array((1, 2, 3, 4, 5, 6)).reshape((3, 2))
            ),
        ]

    @unittest.expectedFailure
    def test_proper_initialization_type_error(self):
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[0])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[1])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[2])

    def test_improper_initialization_type_error(self):
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[3])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[5])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[6])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[7])
        with self.assertRaises(TypeError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[8])

    @unittest.expectedFailure
    def test_proper_initialization_value_error(self):
        with self.assertRaises(ValueError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[0])
        with self.assertRaises(ValueError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[1])
        with self.assertRaises(ValueError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[2])
        with self.assertRaises(ValueError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[3])

    def test_improper_initialization_value_error(self):
        with self.assertRaises(ValueError):
            models.CustomTableModel(TestCustomTableModel.test_data_sets[4])

    def test_row_count(self):
        mdl = models.CustomTableModel(TestCustomTableModel.test_data_sets[0])
        self.assertEqual(mdl.rowCount(), 1)
        mdl = models.CustomTableModel(TestCustomTableModel.test_data_sets[1])
        self.assertEqual(mdl.rowCount(), 1)
        mdl = models.CustomTableModel(TestCustomTableModel.test_data_sets[2])
        self.assertEqual(mdl.rowCount(), 3)
        mdl = models.CustomTableModel(TestCustomTableModel.test_data_sets[9])
        self.assertEqual(mdl.rowCount(), 8)
        mdl = models.CustomTableModel(TestCustomTableModel.test_data_sets[10])
        self.assertEqual(mdl.rowCount(), 3)


# =============================================================================
# Script main body
# =============================================================================

if __name__ == '__main__':
    unittest.main()
