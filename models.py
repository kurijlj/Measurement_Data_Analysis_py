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

from numpy import ndarray
from pandas import read_csv
from collections import namedtuple
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

# We define a custom container for passing raw table data to the custom table
# model.
DataSet = namedtuple('DataSet', ['headers', 'data'])


def checktype(tp, var, vardsc):
    """Utility routine used to check if given variable (var) is of requested
    type (tp). If not it raises TypeError exception with a appropriate message.
    Variable description (vardsc) is used for formatting more descriptive error
    messages when rising exceptions.
    """

    if var is not None and type(var) is not tp:
        raise TypeError('{0} must be {1} or NoneType, not {2}'.format(
            vardsc,
            tp.__name__,
            type(var).__name__
        ))


def color_index(column_index: int, color_count: int):
    """TODO: Put function docstring HERE.
    """

    factor = int(column_index/(color_count-1))
    return column_index - (factor * color_count) + factor + 1


def read_csv_data(fname: str, cobj=None):
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

    def __init__(self, data_set: DataSet = DataSet(None, None)):
        super().__init__()
        self._display_precision = None  # Holds list mapping column indexes to
        # the preffered display precision (decimal places) for the column with
        # a given index. Value of -1 indicates to use default setting (as is in
        # the table and withtwo decimal places on the chart) for displaying
        # column values.
        self._plot = None  # Holds list of boolean values indicating whether
        # the column with given index should be plotted on the chart or not.
        self._color_map = None  # Holds list mapping column indexes to the
        # preset color used for displaying column background and plotting
        # column values on the chart.

        # In the case we are dealing with uninitialized instance of the class
        # or only one vector (column) of data, we set row indexes to represent
        # scale on the X axis and given cell (column) value(s) as Y axis. For
        # that purpose we map value of -1 as column index to X axis to
        # designate that we are using generic scale for the X axis.
        self._x_axis = -1

        # Since objects of this class are instantiated from the main window
        # we assume that main window is providing appropriately formatted data
        # i.e. a tuple or a list consisting of the list containing column
        # headers, and a numpy array containing actual column values (i.e.
        # data table).
        checktype(list, data_set.headers, 'Table header')
        checktype(ndarray, data_set.data, 'Table data')
        self._data_set = data_set  # Holds raw table data

        # Set columns display precision (i.e. number of decimal places) when
        # returning data for display purposes (on Qt.DisplayRole). Default
        # value is -1 denoting to display the value as is in the data table
        # and with two decimal places on the chart.
        if self._data_set.data is not None:

            # By default we set column_count to one.
            column_count = 1

            if len(self._data_set.data.shape) > 1:
                # We are dealing with two dimwnsional data table. So get number
                # of columns in the table. Otherwise we are dealing with an 1D
                # array of data so leave column_count value intact.
                column_count = self._data_set.data.shape[1]

            # If valid types and not None are supplied for both headers and
            # data, check if number of section in headers match number of
            # columns in the data. If they mismatch raise the ValueError.
            if self._data_set.headers is not None:
                section_count = len(self._data_set.headers)
                if section_count != column_count:
                    raise ValueError(
                        'Number of sections ({0}) and columns ({1}) mismatch.'
                        .format(section_count, column_count)
                        )

            self._display_precision = [-1] * column_count
            self._plot = [True] * column_count

            self._color_map = list()
            for column in range(column_count):
                cind = color_index(column, len(_COLOR_PALETTE))
                color = _COLOR_PALETTE[cind]
                self._color_map.append(color)

            if column_count > 1:
                # We are dealing with more than one column so we can,
                # by default use the first column (index=0) as X axis scale,
                # and the second column (index=1) as the Y axis. By default we
                # map X axis to the gray color for distinction, and also we
                # have to exclude column designated as the X axis from the
                # chart plot stack.
                self._x_axis = 0
                self._plot[0] = False
                self._color_map[0] = _COLOR_PALETTE[0]

    def rowCount(self, parent=QModelIndex()):
        """TODO: Put method docstring HERE.
        """

        # In the case table model is not initialized we return ...
        result = 1

        if self._data_set.data is not None:
            result = self._data_set.data.shape[0]

        return result

    def columnCount(self, parent=QModelIndex()):
        """TODO: Put method docstring HERE.
        """

        # In the case table model is not initialized we return ...
        result = 1

        if self._data_set.data is not None\
        and len(self._data_set.data.shape) > 1:
            # Here we are excluding cases when for some reason data table isn't
            # initialized, and we are dealing with only one column of data.
            # If we are dealing with only one column of data shape method of
            # the ndarray returns tuple in the form of (row_count,), and if we
            # try to acces item with index 1 it raises index out of range
            # exception.
            result = self._data_set.data.shape[1]

        return result

    def _headerString(self, section):
        """TODO: Put method docstring HERE.
        """

        if section < 0:
            # The only time when column index is less than zero is in the case
            # we are dealing with one column data set, so we simply return 'X'
            # as the column header.
            header_string = 'X'
            return header_string

        header_string = '{}'.format(section)

        if self._data_set.headers is None:
            # Are we dealing with uninitialized object?
            if self._data_set.data is None:
                return header_string

            # Headers are not set for some reason, but table data may still
            # exist. Check if requested section is header of the X axis.
            if section == self._x_axis:
                # Section is header for the X axis so append additional marking
                # designating we are displaying data for the X axis.
                header_string = header_string + ' [X]'
                return header_string

            if self._plot[section]:
                # Section is header for the column designated to be plotted on
                # the chart, so append additional marking designating we are
                # displaying data to be plotted on the chart.
                header_string = header_string + ' [Y]'
                return header_string

        if self._data_set.headers[section] is None:
            # Headers are set but for some reason value of the given section
            # is set to None. In that case we use section number for header
            # string.
            if section == self._x_axis:
                # Section is header for the X axis so append additional marking
                # designating we are displaying data for the X axis.
                header_string = header_string + ' [X]'
                return header_string

            if self._plot[section]:
                # Section is header for the column designated to be plotted on
                # the chart, so append additional marking designating we are
                # displaying data to be plotted on the chart.
                header_string = header_string + ' [Y]'
                return header_string

        # Headers are set and section header is set.
        header_string = '{}'.format(self._data_set.headers[section])

        if section == self._x_axis:
            # Section is header for the X axis so append additional marking
            # designating we are displaying data for the X axis.
            header_string = header_string + ' [X]'
            return header_string

        if self._plot[section]:
            # Section is header for the column designated to be plotted on
            # the chart, so append additional marking designating we are
            # displaying data to be plotted on the chart.
            header_string = header_string + ' [Y]'
            return header_string

        return header_string

    def headerData(self, section, orientation, role):
        """TODO: Put method docstring HERE.
        """

        if role != Qt.DisplayRole:
            return None

        hdr_data = "{}".format(section)

        if orientation == Qt.Horizontal:
            # By default if column is not designated as X axis, nor for
            # plotting on the chart we simply return column header.
            if self._data_set.headers is not None:
                # We have headers loaded ...
                if self._data_set.headers[section] is not None:
                    # and section header data is not None (just a basic
                    # sanity check).
                    hdr_data = self._data_set.headers[section]

            if section == self._x_axis:
                # Header data for the X axis is beeing requested so we
                # append aditional markings designating that we are displaying
                # data for the X axis.
                if self._x_axis < 0:
                    # This is the case of the one column data table, and X axis
                    # data is generated out of row indexes. In this case we
                    # also have to generate header data out of nothing
                    # so we simply return string 'X' for the column header.
                    hdr_data = 'X'
                else:
                    hdr_data = hdr_data + ' [X]'
            elif self._plot[section]:
                # Header data for the column designated for plotting on the
                # chart is beeing requested so we append aditional markings
                # designating that we are displaying data for the column that
                # should be plotted on the chart.
                hdr_data = hdr_data + ' [Y]'

            return hdr_data

        # If display orintation for the header data is not horizontal we simply
        # return column index as the header data.
        return hdr_data

    def data(self, index, role=Qt.DisplayRole):
        """TODO: Put method docstring HERE.
        """

        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            # String representation of the value for the cell with the given
            # indexes is beeing requested. By default we return string
            # representation of the raw value. If deiplay precision for the
            # cell's column is set then return formatted cell walue according
            # to display precision setting.
            value_string = '{}'.format(self._data_set.data[row, column])

            if self._display_precision[column] > -1:
                value_string = '{0:.{1}f}'.format(
                    self._data_set.data[row, column],
                    self._display_precision[column]
                    )

            return value_string

        if role == Qt.BackgroundRole:
            # Background color for painting cells backgroun is beeing
            # requested. For painting cell's background we use color mapped to
            # the cell's column but wiht slightly lighter tone for better
            # readability of the table data. We achieve this by modifying hue
            # and value of the mapped color.
            hue, sat, val, alpha = self._color_map[column].getHsv()
            sat = int(sat * 0.3)
            val = int(val * 1.4)
            if val > 255:
                # If we get values greater than 255 we are overflowing and
                # constructor will return the error, so we have to reduce value
                # down to 255.
                val = 255

            return QColor.fromHsv(hue, sat, val, alpha)

        if role == Qt.TextAlignmentRole:
            # Cell text alignment is beeing requested. So far we are using
            # default alignment setting.
            return Qt.AlignLeft

        if role == Qt.UserRole:
            # We use UserRole to return tables raw values.
            return self._data_set.data[row, column]

        # Unknown role uspplied so return None.
        return None

    def setDisplayPrecision(self, column, precision):
        """TODO: Put method docstring HERE.
        """

        self._display_precision[column] = precision

        # Send signal to display controls that data display format has been
        # changed.
        self.dataChanged.emit(
            self.index(0, column),
            self.index(self._data_set.data.shape[0], column)
            )

    def displayPrecisionString(self, column):
        """TODO: Put method docstring HERE.
        """

        if column < 0:
            # We are dealing with one column data and precision string for
            # the X axis is beeing requested.
            return '%.1f'
        elif self._display_precision[column] > -1:
            return '%.{0}f'.format(self._display_precision[column])
        return '%.2f'  # Default format string for no set dispplay precision.

    def setX(self, new_xind):
        """TODO: Put method docstring HERE.
        """

        # Get column index of the current X axis, put it on chart plot stack
        # and reset plot color.
        xind = self._x_axis
        cind = color_index(xind, len(_COLOR_PALETTE))
        self._color_map[xind] = _COLOR_PALETTE[cind]
        self.toggle_plot(xind)

        # Assign new X axis, remove it from the chart plot stack, and map it
        # to the X axis display color.
        self._x_axis = new_xind
        self._plot[new_xind] = False
        self._color_map[new_xind] = _COLOR_PALETTE[0]

        # In the case this was the last column on the plot stack we find the
        # first column that is not mapped as X axis and put it on the
        # polot stack.
        if not self.plot_stack:
            for column in range(self._data_set.data.shape[1]):
                if column != new_xind:
                    self.toggle_plot(column)
                    break

        # Emit signal
        self.headerDataChanged.emit(
            Qt.Horizontal,
            new_xind,
            new_xind
            )

    # Rename it to changePlotStatus.
    def toggle_plot(self, cind, plot=True):
        """TODO: Put method docstring HERE.
        """

        self._plot[cind] = plot

    # Rename it to getPlotStatus.
    def plot(self, cind):
        """TODO: Put method docstring HERE.
        """

        return self._plot[cind]

    # Rename it to getX.
    @property
    def x_axis(self):
        """TODO: Put method docstring HERE.
        """

        return self._x_axis

    # This method should be removed.
    @property
    def plot_stack(self):
        """TODO: Put method docstring HERE.
        """

        stack = list()
        for index in range(self._data_set.data.shape[1]):
            if self._plot[index]:
                stack.append(index)

        return tuple(stack)

    # Rename it to getDrawingPen.
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
