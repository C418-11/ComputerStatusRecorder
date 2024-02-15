# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.2Dev"

import sys
import time

import colorama
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from Lib import StdColor
from UI.BaseWidgets import GetScale
from UI.Main import UiMain
from UI import RegisterUI
from UI.tools import showException


def _setOpacity(widget, menubar):

    @showException
    def _gradient(to):
        _from = widget.windowOpacity()
        # 从_from渐变到to
        sub = (to - _from) / 100
        for i in range(100):
            widget.setWindowOpacity(_from + i * sub)
            QApplication.processEvents()
            time.sleep(0.01)

    def _animation(opacity):
        return lambda: _gradient(opacity)

    menu = menubar.addMenu("Opacity")

    for alpha in range(100, 79, -5):
        menu.addAction(str(alpha) + "%", _animation(alpha/100))

    for alpha in range(70, 29, -10):
        menu.addAction(str(alpha) + "%", _animation(alpha/100))

    menubar.addMenu(menu)


def main():
    app = QApplication(sys.argv)
    widget = GetScale()
    ui = UiMain(widget)
    ui.setupUi()
    _setOpacity(widget, ui.MenuBar)

    for w in RegisterUI.widgets:
        ui.append(w)
        pass

    # noinspection PyUnresolvedReferences
    widget.setWindowFlags(Qt.CustomizeWindowHint)
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    sys.stdout = StdColor.ColorWrite(sys.__stdout__, colorama.Fore.LIGHTGREEN_EX)
    print(f"Version: {__version__}")
    print(f"Author: {__author__}")
    print(f"版本号: {__version__}")
    print(f"作者: {__author__}")
    sys.stdout = StdColor.ColorWrite(sys.__stdout__, colorama.Fore.LIGHTYELLOW_EX)
    main()

__all__ = ("main",)
