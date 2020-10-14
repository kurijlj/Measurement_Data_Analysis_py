
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

import datasets
import unittest


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

    @unittest.expectedFailure
    def changePlotStatusTestFail(self):
        """TODO: Put method docstring HERE.
        """
        with self.assertRaises(IndexError):
            TEST_CASES[0].changePlotStatus(-1)
        with self.assertRaises(IndexError):
            TEST_CASES[0].changePlotStatus(1)


# =============================================================================
# Script main body
# =============================================================================

if __name__ == '__main__':
    unittest.main()
