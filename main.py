# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.2Bata"

import sys
import time

import colorama
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

import FeatureLoader
from Lib import StdColor
from UI.BaseWidgets import GetScale
from UI.Main import UiMain
from UI import RegisterUI


def main():
    FeatureLoader.load_default_features()

    app = QApplication(sys.argv)
    widget = GetScale()
    ui = UiMain(widget)
    ui.setupUi()

    for Menu in RegisterUI.menu:
        menu = Menu(widget)
        menu.setupUi()
        ui.MenuBar.addMenu(menu.getMenuWidget())

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
