# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.6Release"

import os
import sys
import traceback

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

    if _load_other_futures.get_default("Load", False) is True:
        try:
            FeatureLoader.load_other_features()
        except Exception as e:
            print("An error occurred while loading another futures:", file=sys.stderr)
            traceback.print_exception(e)

    app = QApplication(sys.argv)
    widget = GetScale()
    ui = UiMain(widget)
    ui.setupUi()

    RegisterUI.menu.sort(key=lambda x: x.priority())
    RegisterUI.widgets.sort(key=lambda x: x.priority())

    for Menu in RegisterUI.menu:
        menu = Menu(ui.MenuBar, widget)
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
