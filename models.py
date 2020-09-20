#!/usr/bin/env python3
"""TODO: Put module docstring HERE.
"""

#==============================================================================
# Copyright (C) 2020 Ljubomir Kurij <kurijlj@gmail.com>
#
# This file is part of mda (Measurement Data Analytics).
#
# This program uses code from Qt for Python examples of the Qt Toolkit
# <https://doc.qt.io/qtforpython/_downloads/06ada84b04e72c9468651471cc91b026/
# datavisualize.tar.bz2> by The Qt Company Ltd., available under a
# 3-Clause BSD License.
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
# 2020-09-19 Ljubomir Kurij <kurijlj@gmail.com>
#
# * mda.py: created.
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
        self.load_data(data_table)

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
            return QColor(Qt.white)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None
