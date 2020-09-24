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
    QInputDialog,
    QMainWindow,
    QMenu,
    QSizePolicy,
    QTableView,
    QWidget
    )
import models


# =============================================================================
# Views classes
# =============================================================================

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

        # Initialize the widget containers.
        self._lyt_objs = dict()  # Layout related objects.
        self._tbl_objs = dict()  # Table view related objects.
        self._crt_objs = dict()  # Chart view related objects.

        # Get the Model.
        self._model = models.CustomTableModel(data)

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

        # TODO: Set up chart axes HERE.
        ###############################

        # Add graph to the chart.
        #########################
        self.add_series('Raw data', (0, 1))

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

    def add_series(self, name, columns):
        """TODO: Put method docstring HERE.
        """

        # Create QLineSeries.
        #####################
        self._crt_objs['series'] = QtCharts.QLineSeries()
        self._crt_objs['series'].setName(name)
        self._crt_objs['series'].setPen(QPen(
            Qt.darkRed,
            0.5,
            Qt.SolidLine,
            Qt.RoundCap,
            Qt.RoundJoin
            ))

        # Filling QLineSeries.
        ######################
        for i in range(self._model.rowCount()):
            # Getting the data
            x = float(self._model.index(i, 0).data(Qt.UserRole))
            y = float(self._model.index(i, 1).data(Qt.UserRole))
            self._crt_objs['series'].append(x, y)

        self._crt_objs['chart'].addSeries(self._crt_objs['series'])

        # Setting X-axis.
        #################
        self._crt_objs['axis_x'] = QtCharts.QValueAxis()
        self._crt_objs['axis_x'].setTickCount(10)
        self._crt_objs['axis_x'].setLabelFormat(
            self._model.display_precision_str(0)
            )
        self._crt_objs['axis_x'].setTitleText(self._model.headerData(
            columns[0],
            Qt.Horizontal,
            Qt.DisplayRole
            ))
        self._crt_objs['chart'].addAxis(
            self._crt_objs['axis_x'],
            Qt.AlignBottom
            )
        self._crt_objs['series'].attachAxis(self._crt_objs['axis_x'])

        # Setting Y-axis.
        #################
        self._crt_objs['axis_y'] = QtCharts.QValueAxis()
        self._crt_objs['axis_y'].setTickCount(10)
        self._crt_objs['axis_y'].setLabelFormat(
            self._model.display_precision_str(1)
            )
        self._crt_objs['axis_y'].setTitleText(self._model.headerData(
            columns[1],
            Qt.Horizontal,
            Qt.DisplayRole
            ))
        self._crt_objs['chart'].addAxis(
            self._crt_objs['axis_y'],
            Qt.AlignLeft
            )
        self._crt_objs['series'].attachAxis(self._crt_objs['axis_y'])

        # Getting the color from the QChart to use it on the QTableView.
        self._model.color = "{}".format(
            self._crt_objs['series'].pen().color().name()
            )

    @Slot()
    def open_horizontal_header_menu(self, pos):
        column = self._tbl_objs['horizontal_header'].logicalIndexAt(pos)

        context_menu = QMenu(self)
        set_precision_action = QAction('Change Display Precision', self)

        # The only way to bundle custom data with the triggered signal is as
        # follows:
        set_precision_action.triggered.connect(
            lambda checked: self.open_set_precision_dialog(
                checked,
                column
                )
            )

        context_menu.addAction(set_precision_action)
        context_menu.addSeparator()
        context_menu.addAction(QAction('Remove Column', self))
        context_menu.popup(
            self._tbl_objs['horizontal_header']\
                    .viewport().mapToGlobal(pos)
            )

    @Slot()
    def open_set_precision_dialog(self, checked, column):
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

        if result[1]:
            self._model.change_display_precision(column, result[0])
            if column == 0:
                self._crt_objs['axis_x'].setLabelFormat(
                    self._model.display_precision_str(0)
                    )
            else:
                self._crt_objs['axis_y'].setLabelFormat(
                    self._model.display_precision_str(1)
                    )


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
