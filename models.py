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
# * Refactor ShowVersionAction class to take fewer attributes. Refactor
#   __init__ to take only one argument a named tuple (VersionDocumentation)
#   that would be passed and store as all relevant version documentation.
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

from pandas import read_csv
from pandas.errors import ParserError
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

# First color in the palette (gray) is reserved for the current X axis
# background painting.
_COLOR_PALETTE = [
    QColor(169, 169, 169, 255), QColor(0, 255, 255, 255),
    QColor(127, 255, 212, 255), QColor(0, 0, 255, 255),
    QColor(138, 43, 226, 255), QColor(165, 42, 42, 255),
    QColor(210, 105, 30, 255), QColor(255, 127, 80, 255),
    QColor(100, 149, 237, 255), QColor(220, 20, 60, 255),
    QColor(0, 0, 139, 255), QColor(0, 139, 139, 255),
    QColor(184, 134, 11, 255), QColor(0, 100, 0, 255),
    QColor(139, 0, 139, 255), QColor(85, 107, 47, 255),
    QColor(255, 140, 0, 255), QColor(153, 50, 204, 255),
    QColor(139, 0, 0, 255), QColor(233, 150, 122, 255),
    QColor(143, 188, 143, 255), QColor(72, 61, 139, 255),
    QColor(148, 0, 211, 255), QColor(255, 20, 147, 255),
    QColor(255, 0, 255, 255), QColor(255, 215, 0, 255),
    QColor(0, 128, 0, 255), QColor(173, 255, 47, 255),
    QColor(34, 139, 34, 255), QColor(75, 0, 130, 255),
    QColor(255, 0, 0, 255)]


# =============================================================================
# Models classes and functions
# =============================================================================

def color_index(column_index, color_count):
    """TODO: Put function docstring HERE.
    """

    factor = int(column_index/(color_count-1))
    return column_index - (factor * color_count) + factor + 1


def read_csv_data(fname, cobj=None):
    """TODO: Put function docstring HERE.
    """

    read_data_frame = None
    headers = None
    data = None

    # Read the CSV content
    try:
        read_data_frame = read_csv(fname)
    except ParserError as err:
        if hasattr(cobj, 'show_error_info'):
            cobj.show_error_info(str(err))
        else:
            print(err)

    if read_data_frame is not None:
        headers = read_data_frame.columns.to_list()
        data = read_data_frame.values

    return headers, data


class CustomTableModel(QAbstractTableModel):
    """TODO: Put class docstring HERE.
    """

    def __init__(self, data_table=None):
        super().__init__()
        self._headers = None
        self._data = None
        self._display_precision = None
        self._plot_on_chart = None
        self._color_map = None

        self.load_data(data_table)

        # Set columns display precision (i.e. number of decimal places) when
        # returning data for display purposes (on Qt.DisplayRole). Default
        # value is -1 denoting to display the value as is.
        if self._headers is not None:
            column_count = len(self._headers)
            self._display_precision = [-1] * column_count
            self._plot_on_chart = [True] * column_count

            self._color_map = list()
            for column in range(self._data.shape[1]):
                cind = color_index(column, len(_COLOR_PALETTE))
                color = _COLOR_PALETTE[cind]
                self._color_map.append(color)

            # By default we use first column (index=0) as X axis so we map it
            # to the gray color in the palette. We also have to exclude X
            # axis from the chart plot stack.
            self._plot_on_chart[0] = False
            self._color_map[0] = _COLOR_PALETTE[0]

        # By default we set index of first column as X axis.
        self._x_axis_index = 0

    def load_data(self, data_table):
        """TODO: Put method docstring HERE.
        """

        self._headers = data_table[0]
        self._data = data_table[1]

    def rowCount(self, parent=QModelIndex()):
        """TODO: Put method docstring HERE.
        """

        return self._data.shape[0]

    def columnCount(self, parent=QModelIndex()):
        """TODO: Put method docstring HERE.
        """

        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        """TODO: Put method docstring HERE.
        """

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return (self._headers)[section]

        return "{}".format(section)

    def data(self, index, role=Qt.DisplayRole):
        """TODO: Put method docstring HERE.
        """

        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            if self._display_precision[column] > -1:
                return '{0:.{1}f}'.format(
                    self._data[row, column],
                    self._display_precision[column]
                    )
            return str(self._data[row, column])

        if role == Qt.UserRole:
            return self._data[row, column]

        if role == Qt.BackgroundRole:
            # For the table background we use 50% lighter colors than original.
            hue, sat, val, alpha = self._color_map[column].getHsv()
            sat = int(sat * 0.3)
            val = int(val * 1.4)
            if val > 255:
                val = 255
            return QColor.fromHsv(hue, sat, val, alpha)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None

    def change_display_precision(self, column, precision):
        """TODO: Put method docstring HERE.
        """

        self._display_precision[column] = precision

    def display_precision_str(self, column):
        """TODO: Put method docstring HERE.
        """

        if self._display_precision[column] > -1:
            return '%.{0}f'.format(self._display_precision[column])
        return '%.2f'  # Default format string for no set dispplay precision.

    def change_x_axis(self, column_index):
        """TODO: Put method docstring HERE.
        """

        # Get column index of the current X axis, put it on chart plot stack
        # and reset plot color.
        xind = self._x_axis_index
        self._plot_on_chart[xind] = True
        cind = color_index(xind, len(_COLOR_PALETTE))
        self._color_map[xind] = _COLOR_PALETTE[cind]

        # Assign new X axis, remove it from the chart plot stack, and map it
        # to the X axis display color.
        self._x_axis_index = column_index
        self._plot_on_chart[column_index] = False
        self._color_map[column_index] = _COLOR_PALETTE[0]

    @property
    def x_axis_index(self):
        """TODO: Put method docstring HERE.
        """

        return self._x_axis_index

    @property
    def plot_stack(self):
        """TODO: Put method docstring HERE.
        """

        stack = list()
        for index in range(self._data.shape[1]):
            if self._plot_on_chart[index]:
                stack.append(index)

        return tuple(stack)

    def drawing_pen(self, column):
        """TODO: Put method docstring HERE.
        """

        pen = QPen(
            self._color_map[column],
            0.5,
            Qt.SolidLine,
            Qt.RoundCap,
            Qt.RoundJoin
            )
        return pen
