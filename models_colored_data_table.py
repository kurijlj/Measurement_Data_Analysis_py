#!/usr/bin/env python3
"""TODO: Put module docstring HERE.
"""

#==============================================================================
# <one line to give the program's name and a brief idea of what it does.>
#
#  Copyright (C) <yyyy> <Author Name> <author@mail.com>
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
#==============================================================================


#==============================================================================
#
# <Put documentation here>
#
# <yyyy>-<mm>-<dd> <Author Name> <author@mail.com>
#
# * <programfilename>.py: created.
#
#==============================================================================


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
from PySide2.QtCore import(
    QAbstractTableModel,
    QModelIndex,
    Qt
    )
from PySide2.QtGui import QColor


#==============================================================================
# Models classes and functions
#==============================================================================

def color_index(column_index, palette_len):
    """TODO: Put function docstring HERE.
    """

    factor = int(column_index/(palette_len-1))
    return column_index - (factor * palette_len) + factor + 1


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

    color_palette= [
        QColor(169, 169, 169, 255), QColor(0, 255, 255, 255),
        QColor(127, 255, 212, 255), QColor(0, 0, 255, 255),
        QColor(138, 43, 226, 255), QColor(165, 42, 42, 255),
        QColor(210, 105, 30, 255), QColor(255, 127, 80, 255)]

    color_palette_old = [
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

    def __init__(self, data_table=None):
        super().__init__()
        self._headers = None
        self._data = None
        self._color_map = list()

        self.load_data(data_table)
        for column in range(self._data.shape[1]):
            color = CustomTableModel.color_palette[
                color_index(column, len(CustomTableModel.color_palette))]
            self._color_map.append(color) 

        # By default we use first column (index=0) as X axis so we map it to
        # the gray color in the palette.
        self._color_map[0] = CustomTableModel.color_palette[0]

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
            return str(self._data[row, column])

        if role == Qt.BackgroundRole:
            # For the table background we use 50% lighter colors than original.
            hue, sat, val, alpha = self._color_map[column].getHsv()
            sat = int(sat * 0.3)
            val = int(val * 1.4)
            if val > 255:
                val = 255
            return QColor.fromHsv(hue, sat, val, alpha)
            # return self._color_map[column].lighter(150)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None
