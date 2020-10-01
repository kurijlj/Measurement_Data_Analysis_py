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

from os import getcwd
from enum import Enum
from os.path import basename
from PySide2.QtCharts import QtCharts
from PySide2.QtCore import (
    Qt,
    Slot
    )
from PySide2.QtGui import (
    QKeySequence,
    QPainter
    )
from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
    QSizePolicy,
    QTableView,
    QWidget
    )
import models


# =============================================================================
# Views classes
# =============================================================================

class Axis(Enum):
    """TODO: Put class docstring HERE.
    """

    X = 0,
    Y = 1


class MainWindow(QMainWindow):
    """TODO: Put class docstring HERE.
    """

    def __init__(self):
        super().__init__()
        self._menu = dict()
        self._actions = dict()
        self._stat_bar = None

        self.setWindowTitle("Data Visualisation with Qt")
        self._init_menu()
        self._init_actions()
        self._init_status_bar()

        # Window dimensions.
        ####################
        # Set window size to 80% of available screen width and 70% of
        # available screen height.
        #############################################################
        geometry = QApplication.desktop().geometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

    def _init_menu(self):
        self._menu['menu_bar'] = self.menuBar()
        self._menu['file_menu'] = self._menu['menu_bar'].addMenu('File')

    def _init_actions(self):
        # File open action.
        ###################
        file_open_action = QAction('Open', self)
        file_open_action.setShortcut(QKeySequence.Open)
        file_open_action.triggered.connect(self.open_file)

        # Exit action.
        ##############
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Add actions to menu.
        ######################
        self._menu['file_menu'].addAction(file_open_action)
        self._menu['file_menu'].addSeparator()
        self._menu['file_menu'].addAction(exit_action)

    def _init_status_bar(self):
        self._stat_bar = self.statusBar()
        self._stat_bar.showMessage('Ready')

    def open_file(self):
        """TODO: Put method docstring HERE.
        """

        files = None
        headers = None
        data = None

        self.update_status_bar('Opening a file ...')
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter('Comma-separated values (*.csv)')
        dlg.setViewMode(QFileDialog.Detail)
        dlg.setDirectory(getcwd())

        if dlg.exec():
            files = dlg.selectedFiles()
            file_name = basename(files[0])
            self.update_status_bar('File selected: {0}'.format(file_name))
            self.update_status_bar('Loading data ...')
            headers, data = models.read_csv_data(files[0], self)
        else:
            self.update_status_bar('No file selected')

        if data is not None:
            data_view = DataViewWidget(models.DataSet(headers, data))
            self.setCentralWidget(data_view)
            self.update_status_bar('Ready')

        # Give focus back to the main app window.
        self.activateWindow()

    def update_status_bar(self, msg):
        """TODO: Put method docstring HERE.
        """

        self._stat_bar.showMessage(msg)

    def show_error_info(self, info):
        """TODO: Put method docstring HERE.
        """

        # So far we are only displaying error info in the status bar.
        self.update_status_bar(info)


class DataViewWidget(QWidget):
    """TODO: Put class docstring HERE.
    """

    def __init__(self, data_set):
        super().__init__()

        # Initialize the widget containers.
        self._lyt_objs = dict()  # Layout related objects.
        self._tbl_objs = dict()  # Table view related objects.
        self._crt_objs = dict()  # Chart view related objects.

        # Get the Model.
        self._model = models.CustomTableModel(data_set)

        # Create a QTableView.
        ######################
        self._tbl_objs['table_view'] = QTableView()
        self._tbl_objs['table_view'].setModel(self._model)

        # QTableView Horizontal Header.
        ###############################
        self._tbl_objs['horizontal_header']\
            = self._tbl_objs['table_view'].horizontalHeader()
        self._tbl_objs['horizontal_header'].setSectionResizeMode(
            QHeaderView.ResizeToContents
            )

        # Enable Context Menu for the Horizontal Header.
        self._tbl_objs['horizontal_header'].setContextMenuPolicy(
            Qt.CustomContextMenu
            )
        self._tbl_objs['horizontal_header'].customContextMenuRequested\
            .connect(self.open_horizontal_header_menu)

        # Vertical Header.
        ##################
        self._tbl_objs['vertical_header']\
            = self._tbl_objs['table_view'].verticalHeader()
        self._tbl_objs['vertical_header'].setSectionResizeMode(
            QHeaderView.ResizeToContents
            )
        self._tbl_objs['horizontal_header'].setStretchLastSection(True)

        # Creating QChart.
        ##################
        self._crt_objs['chart'] = QtCharts.QChart()
        self._crt_objs['chart'].setAnimationOptions(
            QtCharts.QChart.AllAnimations
            )

        # Adding series to the chart.
        ##################
        self.add_series()

        # Adding axes to the chart.
        ##################
        self.add_axis(Axis.X)
        self.add_axis(Axis.Y)

        # Creating QChartView.
        ######################
        self._crt_objs['chart_view'] = QtCharts.QChartView(
            self._crt_objs['chart'])
        self._crt_objs['chart_view'].setRenderHint(QPainter.Antialiasing)

        # QWidget Layout.
        #################
        self._lyt_objs['main_layout'] = QHBoxLayout()

        # Set size policy for the table view and the chart.
        ###################################################
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        self._tbl_objs['table_view'].setSizePolicy(size)
        size.setHorizontalStretch(4)
        self._crt_objs['chart_view'].setSizePolicy(size)

        # Left layout.
        ##############
        self._lyt_objs['main_layout'].addWidget(
            self._tbl_objs['table_view']
            )

        # Right Layout.
        ###############
        self._lyt_objs['main_layout'].addWidget(
            self._crt_objs['chart_view']
            )

        # Set the layout to the QWidget.
        ################################
        self.setLayout(self._lyt_objs['main_layout'])

    def add_series(self):
        """TODO: Put method docstring HERE.
        """

        xind = self._model.x_axis
        for plottable in self._model.plot_stack:
            series = QtCharts.QLineSeries()
            series.setName(self._model.headerData(
                plottable,
                Qt.Horizontal,
                Qt.DisplayRole
                ))
            series.setPen(self._model.drawing_pen(plottable))
            for i in range(self._model.rowCount()):
                # Getting the data
                if xind == -1:
                    # We are dealing with only one vector of data so use
                    # row indexes as X axis.
                    x = float(i)
                else:
                    x = float(self._model.index(i, xind).data(Qt.UserRole))
                y = float(self._model.index(i, plottable).data(Qt.UserRole))
                series.append(x, y)

            self._crt_objs['chart'].addSeries(series)

    def add_axis(self, which_axis):
        """TODO: Put method docstring HERE.
        """

        axind = self._model.x_axis
        alignment = Qt.AlignBottom
        if which_axis == Axis.Y:
            # We use first column in the plot stack to draw the y axis.
            axind = self._model.plot_stack[0]
            alignment = Qt.AlignLeft
        axis = QtCharts.QValueAxis()
        axis.setTickCount(10)
        axis.setLabelFormat(self._model.displayPrecisionString(axind))
        axis.setTitleText(self._model.headerData(
            axind,
            Qt.Horizontal,
            Qt.DisplayRole
            ))
        self._crt_objs['chart'].addAxis(axis, alignment)

        # Assign axis to all series on the chart.
        for serie in self._crt_objs['chart'].series():
            serie.attachAxis(axis)

    @Slot()
    def open_horizontal_header_menu(self, pos):
        """TODO: Put method docstring HERE.
        """

        column = self._tbl_objs['horizontal_header'].logicalIndexAt(pos)
        selected_indexes = self._tbl_objs['table_view'].selectedIndexes()
        selected_columns = set()
        if selected_indexes:
            for index in selected_indexes:
                selected_columns.add(index.column())
        else:
            selected_columns.add(column)

        context_menu = QMenu(self)

        # Set precision action.
        set_precision_action = QAction('Change Display Precision', self)
        # The only way to bundle custom data with the triggered signal is as
        # follows:
        set_precision_action.triggered.connect(
            lambda checked: self.open_set_precision_dialog(
                checked,
                selected_columns
                )
            )
        context_menu.addAction(set_precision_action)

        # Set as X axis action.
        setx_axis_action = QAction('Set as X Axis', self)
        if self._model.columnCount() < 2\
                or len(selected_columns) > 1\
                or self._model.x_axis in selected_columns:
            # We have only one column so we can't use it as X axis, or selected
            # column have already been mapped as X axis.
            setx_axis_action.setEnabled(False)
        else:
            setx_axis_action.triggered.connect(
                lambda checked: self.setX(
                    checked,
                    selected_columns
                    )
                )
        context_menu.addAction(setx_axis_action)

        # Set plot switch action.
        toggle_plot_action = QAction('Plot', self)
        if self._model.columnCount() < 3\
                or self._model.x_axis in selected_columns:
            # We have only one column so we can't toggle plot off (we need that
            # data on the graph, or column is mapped as X axis (again we can't
            # toggle plot on or off).
            toggle_plot_action.setEnabled(False)
        else:
            toggle_plot_action.triggered.connect(
                lambda checked: self.toggle_plot(
                    checked,
                    selected_columns
                    )
                )
        context_menu.addAction(toggle_plot_action)

        context_menu.addSeparator()

        context_menu.addAction(QAction('Remove Column', self))

        context_menu.popup(
            self._tbl_objs['horizontal_header']
                    .viewport().mapToGlobal(pos)
            )

    @Slot()
    def open_set_precision_dialog(self, checked, columns):
        """TODO: Put method docstring HERE.
        """

        self.parent().update_status_bar('Changing display precision ...')

        # result is a tuple containing value for the input field and boolean
        # value indicating whether dialog OK or Cancel button has been hit
        # (OK == True, Cancel == False).
        result = QInputDialog.getInt(
            self,
            'Display Precision Settings',  # title
            'Decimal places to show:',     # label
            0,                             # value
            0,                             # minValue
            20,                            # maxValue
            1                              # step
            )

        y_rep = True  # Flag controling if Y axis has already been redrawn.
        if result[1]:
            for column in columns:
                self._model.setDisplayPrecision(column, result[0])
                if result[0] and column == self._model.x_axis:
                    self._crt_objs['chart'].removeAxis(
                        self._crt_objs['chart'].axisX()
                        )
                    self.add_axis(Axis.X)
                elif result[0] and y_rep:
                    self._crt_objs['chart'].removeAxis(
                        self._crt_objs['chart'].axisY()
                        )
                    self.add_axis(Axis.Y)
                    y_rep = False

        self.parent().update_status_bar('Changing display precision ...')
        self.parent().update_status_bar('Ready')

    @Slot()
    def setX(self, checked, columns):
        """TODO: Put method docstring HERE.
        """

        self._model.setX(columns.pop())
        self.parent().update_status_bar('Changing X axis ...')

        # First let remove all axes and series from the chart.
        self._crt_objs['chart'].removeAllSeries()
        self._crt_objs['chart'].removeAxis(
            self._crt_objs['chart'].axisX()
            )
        self._crt_objs['chart'].removeAxis(
            self._crt_objs['chart'].axisY()
            )

        # Do the chart redrawing.
        self.add_series()
        self.add_axis(Axis.X)
        self.add_axis(Axis.Y)

        self.parent().update_status_bar('Ready')

    @Slot()
    def toggle_plot(self, checked, columns):
        """TODO: Put method docstring HERE.
        """

        self.parent().update_status_bar('Updating plot ...')

        for column in columns:
            plot = not self._model.plot_on_chart(column)
            series_name = self._model.headerData(
                column,
                Qt.Horizontal,
                Qt.DisplayRole
                )
            self._model.toggle_plot(column, plot)

            if plot:
                xind = self._model.x_axis
                series = QtCharts.QLineSeries()
                series.setName(self._model.headerData(
                    column,
                    Qt.Horizontal,
                    Qt.DisplayRole
                    ))
                series.setPen(self._model.drawing_pen(column))
                for i in range(self._model.rowCount()):
                    xval = float(self._model.index(i, xind).data(Qt.UserRole))
                    yval = float(
                        self._model.index(i, column).data(Qt.UserRole)
                        )
                    series.append(xval, yval)

                self._crt_objs['chart'].addSeries(series)

            else:
                for series in self._crt_objs['chart'].series():
                    if series_name == series.name():
                        self._crt_objs['chart'].removeSeries(series)

        self.parent().update_status_bar('Ready')


# =============================================================================
# GUI launcher
# =============================================================================

def run_main_view():
    """TODO: Put function docstring HERE.
    """

    gui_instance = QApplication([])
    main_view = MainWindow()
    main_view.show()

    return gui_instance.exec_()
