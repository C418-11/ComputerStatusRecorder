# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

import time

from PyQt5.QtWidgets import QApplication, QMenuBar, QMenu

from UI.ABC import AbcMenu
from UI.tools import showException
from UI.RegisterUI import register_menu


class OpacityMenu(AbcMenu):
    def __init__(self, _parent):
        super().__init__(_parent)
        self.widget = _parent
        self.menu: QMenu | None = None

    @showException
    def _gradient(self, to):
        _from = self.widget.windowOpacity()
        # 从_from渐变到to
        sub = (to - _from) / 100
        for i in range(100):
            self.widget.setWindowOpacity(_from + i * sub)
            QApplication.processEvents()
            time.sleep(0.01)

    def getMenuWidget(self):
        return self.menu

    def setupUi(self):
        self.menu = QMenu(self.widget)
        self.menu.setTitle("Opacity")

        def _animation(opacity):
            return lambda: self._gradient(opacity)

        for alpha in range(100, 79, -5):
            self.menu.addAction(str(alpha) + "%", _animation(alpha/100))

        for alpha in range(70, 29, -10):
            self.menu.addAction(str(alpha) + "%", _animation(alpha/100))


register_menu(OpacityMenu)
