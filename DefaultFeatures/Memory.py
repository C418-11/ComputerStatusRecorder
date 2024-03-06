# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.2Dev"

import os
import threading
import time
import warnings
from threading import Thread
from typing import override

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QLabel, QPushButton

from Lib.Configs import read_default_yaml, BASE_PATH, MinimumSize
from Lib.Configs import FontFamily, TitleFont, SmallFont
from Recorder.Memory import Memory as RMemory, PathType
from Recorder.tools import time_str as _time_str
from UI.ABC import AbcUI
from UI.BaseWidgets import MatplotlibWidget
from UI.RegisterUI import register
from UI.tools import showException


def _render_plot(ax, color, used):
    # cover 将 [(x1, y1), (x2, y2), ...] 转换为 ([x1, x2, ...,], [y1, y2, ...])
    def _cover(ls):
        x = [t for t, _ in ls]
        y = [v for _, v in ls]
        return x, y

    ax.plot(*_cover(used), color=color, label='Used')

    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Bytes')

    ax.legend(loc='upper left', fontsize=SmallFont)


class Memory(AbcUI):
    _configs = read_default_yaml(os.path.join(BASE_PATH, 'Memory.yaml'), {
        "[Show]": {
            "Max Record": 50,
            "Record Delay": 0.5,
            "Fill Default": True,
            "LineColor": "blue",
            "Path": r"./.record/Memory/",
        },
        "[Record]": {
            "Max Record": 50,
            "Record Delay": 0.5,
            "Path": r"./.record/Memory/",
        },
    })

    def __init__(self, parent: QTabWidget):
        super().__init__(parent)
        self.Widget = parent
        self.tag_widget: QWidget | None = None

        self.TextLabel: QLabel | None = None

        self.plot_widget: MatplotlibWidget | None = None

        self.SaveFileButton: QPushButton | None = None
        self.SavePlotButton: QPushButton | None = None

        self.PlotRenderLock = threading.Lock()
        self.PlotRecordLock = threading.Lock()

        self.show_getter = RMemory(
            max_record_len=self._configs["[Show]"]["Max Record"],
            save_path=self._configs["[Show]"]["Path"]
        )

        self.record_getter = RMemory(
            max_record_len=self._configs["[Record]"]["Max Record"],
            save_path=self._configs["[Record]"]["Path"]
        )

        self.running = False
        self._show_thread = Thread(target=self._show_loop, daemon=True, name=f"{type(self).__name__}--ShowThread")
        self._record_thread = Thread(target=self._record_loop, daemon=True, name=f"{type(self).__name__}--RecordThread")

        self.base_wh: tuple[int, int] | None = None

    @showException
    def _save_record(self, *_):
        with self.PlotRecordLock:
            file_paths = self.record_getter.save()
            file_paths: dict[PathType, str]

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Tip")
        msg_box.setIcon(QMessageBox.Information)

        path_str = [f"{k}: {v}" for k, v in file_paths.items()]

        msg_box.setText("Do you want to open the folder in which the file is saved?\n\n"
                        "File saved:\n" + "\n".join(path_str))

        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        response = msg_box.exec()
        if response == QMessageBox.Ok:
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.join(self.record_getter.save_path, ".MemoryRecord")))

    @showException
    def _save_show_plot(self, *_):
        dir_path = os.path.join(self.show_getter.save_path, ".PlotImage")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        start_time = _time_str("%Y-%m-%d--%H-%M-%S", self.show_getter.start_time)
        finish_str = _time_str("%Y-%m-%d--%H-%M-%S", time.time_ns())
        life = f"Time[Start[{start_time}],Finish[{finish_str}]]"

        file_path = os.path.join(dir_path, f"{life}.png")

        with self.PlotRenderLock:
            self.plot_widget.figure.savefig(file_path)

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Tip")
        msg_box.setIcon(QMessageBox.Information)

        msg_box.setText("Do you want to open the saved picture?\n\n"
                        "File saved:\n"
                        f"  {dir_path}")

        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        response = msg_box.exec()
        if response == QMessageBox.Ok:
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

    @override
    def ReScale(self, x_scale: float, y_scale: float):
        self.PlotRenderLock.acquire()

        self.plot_widget.resize(int(self.base_wh[0] * x_scale), int(self.base_wh[1] * y_scale))

        self.TextLabel.resize(int(MinimumSize[0] * x_scale), int(40 * y_scale))
        self.TextLabel.move(0, 0)
        self.TextLabel.setAlignment(Qt.AlignCenter)

        self.SaveFileButton.resize(int(100 * x_scale), int(30 * y_scale))
        self.SavePlotButton.resize(int(100 * x_scale), int(30 * y_scale))

        self.SaveFileButton.move(0, self.plot_widget.height() - self.SavePlotButton.height())

        self.SavePlotButton.move(
            self.SaveFileButton.width(),
            self.SaveFileButton.y()
        )

        self.PlotRenderLock.release()

    @override
    def setupUi(self):
        self.tag_widget = QWidget(self.Widget)
        self.tag_widget.setObjectName("Memory")
        self.plot_widget = MatplotlibWidget(self.tag_widget)
        self.plot_widget.setObjectName("MemoryPlot")

        self.plot_widget.move(0, 0)

        self.base_wh = MinimumSize[0] - 10, MinimumSize[1] - 50
        self.plot_widget.resize(*self.base_wh)

        self.TextLabel = QLabel(self.tag_widget)
        self.TextLabel.setFont(QFont(FontFamily, TitleFont))
        self.TextLabel.setObjectName("MemoryLabel")
        self.TextLabel.setAlignment(Qt.AlignCenter)

        self.SaveFileButton = QPushButton(self.tag_widget)
        self.SaveFileButton.setObjectName("SaveFileButton")
        self.SaveFileButton.setText("Save File")

        self.SavePlotButton = QPushButton(self.tag_widget)
        self.SavePlotButton.setObjectName("SavePlotButton")
        self.SavePlotButton.setText("Save Plot")

        # noinspection PyUnresolvedReferences
        self.SaveFileButton.clicked.connect(self._save_record)
        # noinspection PyUnresolvedReferences
        self.SavePlotButton.clicked.connect(self._save_show_plot)

        self.running = True
        self._record_thread.start()
        self._show_thread.start()

    def _show_loop(self):
        ax = self.plot_widget.figure.subplots()
        self.ax = ax

        if self._configs["[Show]"].get_default("Fill Default", True):
            config_show = self._configs["[Show]"]
            record_delay = int(config_show["Record Delay"] * 1000000000)

            stop = time.time_ns()
            start = int(stop - (config_show["Max Record"] * record_delay))

            for past_timestamp in range(start, stop, record_delay):
                self.show_getter.used_que.append((past_timestamp, 0))

        def _once():
            self.show_getter.update()

            self.TextLabel.setText(
                f"Free: {round(self.show_getter.free_unit[0], 2)} {self.show_getter.free_unit[1].abbreviation}  "
                f"  Used: {round(self.show_getter.used_unit[0], 2)} {self.show_getter.used_unit[1].abbreviation}"
            )

            with self.PlotRenderLock:
                ax.clear()
                _render_plot(ax, self._configs["[Show]"].get_default("LineColor", "blue"), self.show_getter.used_que)

            self.plot_widget.canvas.draw()

            time.sleep(self._configs["[Show]"]["Record Delay"])

        while self.running:
            try:
                _once()
            except RuntimeError as err:
                if "C/C++" in str(err) and "delete" in str(err):
                    if not self.running:
                        return
                    try:
                        warnings.warn(
                            "The program appears to be closed, stopping the drawing loop...",
                            RuntimeWarning,
                            stacklevel=1
                        )
                    except RuntimeError:
                        pass
                    return
                else:
                    raise

    def _record_loop(self):
        while self.running:
            with self.PlotRenderLock:
                self.record_getter.update()
            time.sleep(self._configs["[Record]"]["Record Delay"])

    @override
    def getMainWidget(self):
        return self.tag_widget

    @override
    def getTagName(self):
        return self.tag_widget.objectName()

    @staticmethod
    @override
    def priority():
        return -1

    @override
    def exit(self):
        self.running = False


register(Memory)
