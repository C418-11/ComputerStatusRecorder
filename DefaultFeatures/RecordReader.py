# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

import csv
import os
import struct

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTabWidget, QWidget, QPushButton, QLabel, QMessageBox
from PyQt5.QtWidgets import QFileDialog

from UI.ABC import AbcUI
from UI.RegisterUI import register

from Lib.Configs import FontFamily, SmallFont
from UI.tools import showException

import time


def _record_reader(_file_path):
    with open(_file_path, 'rb') as f:
        fmt_ls = f.readline().decode()[:-1].split('|')
        size_ls = [struct.calcsize(fmt) for fmt in fmt_ls]

        while True:
            chunk_ls = []
            for size, fmt in zip(size_ls, fmt_ls):
                data = f.read(size)
                if not data:
                    break
                chunk_ls.append(struct.unpack(fmt, data)[0])

            if chunk_ls:
                yield chunk_ls
            else:
                break


class RecordReader(AbcUI):
    def __init__(self, _parent: QTabWidget):
        super().__init__(_parent)

        self._parent = _parent
        self.widget: QWidget | None = None
        self.OpenFileBtn: QPushButton | None = None
        self.FileNameLabel: QLabel | None = None

        self.SaveCSVBtn: QPushButton | None = None
        self.ShowPlotBth: QPushButton | None = None

        self.file_iter_builder = None
        self.file_name: str | None = None

        self.base_size: QSize | None = None

        self._inited_ui = False

    def _openfile(self):
        root_dir = "./.record"
        if not os.path.exists(root_dir):
            root_dir = '.'

        file_path, _ = QFileDialog.getOpenFileName(self.widget, "Open File", root_dir, "All Files (*)")

        if file_path:
            self.file_iter_builder = lambda: _record_reader(file_path)
            self.file_name = os.path.basename(file_path)

            self.FileNameLabel.setText(self.file_name)
            self.FileNameLabel.adjustSize()

    def setupUi(self):
        self.widget = QWidget(self._parent)
        self.widget.resize(self._parent.width(), self._parent.height())

        self.OpenFileBtn = QPushButton(self.widget)
        self.OpenFileBtn.setText("Open File")
        # noinspection PyUnresolvedReferences
        self.OpenFileBtn.clicked.connect(self._openfile)

        self.FileNameLabel = QLabel(self.widget)
        self.FileNameLabel.setFont(QFont(FontFamily, SmallFont))
        self.FileNameLabel.setText("No file selected")
        self.FileNameLabel.adjustSize()
        self.FileNameLabel.setAlignment(Qt.AlignCenter)

        self.SaveCSVBtn = QPushButton(self.widget)
        self.SaveCSVBtn.setText("Save CSV")
        # noinspection PyUnresolvedReferences
        self.SaveCSVBtn.clicked.connect(lambda *_: self._save_to_csv())

        self.ShowPlotBth = QPushButton(self.widget)
        self.ShowPlotBth.setText("Show Plot")
        # noinspection PyUnresolvedReferences
        self.ShowPlotBth.clicked.connect(lambda *_: self._show_plot())

    @showException
    def _save_to_csv(self):
        if self.file_iter_builder is None:
            QMessageBox.warning(self.widget, "Warning", "Please open a file first.")
            return

        root_dir = "./.record"
        if not os.path.exists(root_dir):
            root_dir = '.'

        file_path, _ = QFileDialog.getSaveFileName(
            self.widget,
            "Save File",
            f"{root_dir}/{self.file_name}",
            "CSV Files (*.csv)"
        )

        if file_path:
            print("Saving to:", file_path)
            start_time = time.time()
            with open(file_path, "w") as f:
                writer = csv.writer(f, lineterminator='\n')
                for data in self.file_iter_builder():
                    writer.writerow(data)
            print(f"Saved in {time.time() - start_time:.3f}s")

    @showException
    def _show_plot(self):
        if self.file_iter_builder is None:
            QMessageBox.warning(self.widget, "Warning", "Please open a file first.")
            return

        import matplotlib.pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.set_title(self.file_name)
        ax.grid(True)

        data_ls = []

        print("Building data list...")
        start_time = time.time()
        for data in self.file_iter_builder():
            data_ls.append(data)

        timestamp_value = [x[0] for x in data_ls], [x[1] for x in data_ls]
        print(f"Done! # Took {time.time() - start_time:.3f}s to build data list.")

        ax.plot(*timestamp_value)

        ax.plot()

        plt.ion()
        fig.show(warn=False)

    def getMainWidget(self):
        return self.widget

    def getTagName(self):
        return "Record Reader"

    def ReScale(self, x_scale: float, y_scale: float):
        if not self._inited_ui:
            self.widget.resize(self._parent.width() - 6, self._parent.height() - 25)
            self._inited_ui = True

        self.OpenFileBtn.resize(int(100 * x_scale), int(30 * y_scale))
        self.OpenFileBtn.move(
            int((self.widget.width() - self.OpenFileBtn.width()) / 2),
            int((self.widget.height() - self.OpenFileBtn.height()) / 2) - int(47 * y_scale)
        )

        self.FileNameLabel.move(
            0,
            self.OpenFileBtn.y() + self.OpenFileBtn.height() + int(12 * y_scale)
        )
        self.FileNameLabel.setFixedWidth(self.widget.width())

        self.SaveCSVBtn.resize(int(100 * x_scale), int(30 * y_scale))
        self.ShowPlotBth.resize(int(100 * x_scale), int(30 * y_scale))

        self.SaveCSVBtn.move(0, self.widget.height() - self.SaveCSVBtn.height())
        self.ShowPlotBth.move(self.SaveCSVBtn.width(), self.SaveCSVBtn.y())

    @staticmethod
    def priority():
        return float("inf")


register(RecordReader)
