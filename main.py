# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.3Release"

import os
import sys

import colorama
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import FeatureLoader
from Lib import StdColor
from Lib.Configs import read_default_yaml, BASE_PATH
from UI import RegisterUI
from UI.BaseWidgets import GetScale
from UI.Main import UiMain

_load_other_futures = read_default_yaml(
    os.path.join(BASE_PATH, 'FuturesLoad.yaml'),
    {
        "Load": True,
    }
)


def main():
    FeatureLoader.load_default_features()

    if _load_other_futures["Load"]:
        FeatureLoader.load_other_features()

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
