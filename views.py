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

from os import getcwd
from os.path import basename
from PySide2.QtCharts import QtCharts
from PySide2.QtCore import (
    Qt,
    Slot
    )
from PySide2.QtGui import (
    QKeySequence,
    QPainter,
    QPen
    )
from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QMainWindow,
    QSizePolicy,
    QTableView,
    QWidget
    )
import models


#==============================================================================
# Views classes
#==============================================================================

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

        # Window dimensions - Set window size to 80% of available screen width
        # and 70% of available screen height.
        # screen = QScreen(self)
        # geometry = screen.geometry()
        geometry = QApplication.desktop().geometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

    def _init_menu(self):
        self._menu['menu_bar'] = self.menuBar()
        self._menu['file_menu'] = self._menu['menu_bar'].addMenu('File')

    def _init_actions(self):
        # File open action.
        file_open_action = QAction('Open', self)
        file_open_action.setShortcut(QKeySequence.Open)
        file_open_action.triggered.connect(self.open_file)

        # Exit action.
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Add actions to menu.
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
        else:
            self.update_status_bar('No file selected')

        self.update_status_bar('Loading data ...')
        headers, data = models.read_csv_data(files[0], self)

        if data is not None:
            data_view = DataViewWidget((headers, data))
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

    def __init__(self, data):
        super().__init__()

        # Getting the Model
        self._model = models.CustomTableModel(data)

        # Creating a QTableView
        self._table_view = QTableView()
        self._table_view.setModel(self._model)

        # QTableView Headers
        self._horizontal_header = self._table_view.horizontalHeader()
        self._vertical_header = self._table_view.verticalHeader()
        self._horizontal_header.setSectionResizeMode(
                               QHeaderView.ResizeToContents
                               )
        self._vertical_header.setSectionResizeMode(
                             QHeaderView.ResizeToContents
                             )
        self._horizontal_header.setStretchLastSection(True)

        # Creating QChart
        self._chart = QtCharts.QChart()
        self._chart.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.add_series('Raw data', [0, 1])

        # Creating QChartView
        self._chart_view = QtCharts.QChartView(self._chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        # QWidget Layout
        self._main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left layout
        size.setHorizontalStretch(1)
        self._table_view.setSizePolicy(size)
        self._main_layout.addWidget(self._table_view)

        # Right Layout
        size.setHorizontalStretch(4)
        self._chart_view.setSizePolicy(size)
        self._main_layout.addWidget(self._chart_view)

        # Set the layout to the QWidget
        self.setLayout(self._main_layout)

    def add_series(self, name, columns):
        """TODO: Put method docstring HERE.
        """

        # Create QLineSeries
        self._series = QtCharts.QLineSeries()
        self._series.setName(name)
        self._series.setPen(QPen(
            Qt.darkRed,
            0.5,
            Qt.SolidLine,
            Qt.RoundCap,
            Qt.RoundJoin
            ))

        # Filling QLineSeries
        for i in range(self._model.rowCount()):
            # Getting the data
            x = float(self._model.index(i, 0).data())
            y = float(self._model.index(i, 1).data())
            self._series.append(x, y)

        self._chart.addSeries(self._series)

        # Setting X-axis
        self._axis_x = QtCharts.QValueAxis()
        self._axis_x.setTickCount(10)
        self._axis_x.setLabelFormat('%.4f')
        self._axis_x.setTitleText(self._model.headerData(
            columns[0],
            Qt.Horizontal,
            Qt.DisplayRole
            ))
        self._chart.addAxis(self._axis_x, Qt.AlignBottom)
        self._series.attachAxis(self._axis_x)

        # Setting Y-axis
        self._axis_y = QtCharts.QValueAxis()
        self._axis_y.setTickCount(10)
        self._axis_y.setLabelFormat('%.4f')
        self._axis_y.setTitleText(self._model.headerData(
            columns[1],
            Qt.Horizontal,
            Qt.DisplayRole
            ))
        self._chart.addAxis(self._axis_y, Qt.AlignLeft)
        self._series.attachAxis(self._axis_y)

        # Getting the color from the QChart to use it on the QTableView
        self._model.color = "{}".format(self._series.pen().color().name())


#==============================================================================
# GUI launcher
#==============================================================================

def run_main_view():
    """TODO: Put function docstring HERE.
    """

    gui_instance = QApplication([])
    main_view = MainWindow()
    main_view.show()

    return gui_instance.exec_()
