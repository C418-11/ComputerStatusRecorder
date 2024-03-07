# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTabWidget, QLabel, QWidget

# 导入抽象类，用于继承
from UI.ABC import AbcUI
from UI.RegisterUI import register


# 继承抽象类，实现具体功能
class HelloWorld(AbcUI):
    def __init__(self, _parent: QTabWidget):
        super().__init__(_parent)

        self.widget: QWidget | None = None
        self.Label: QLabel | None = None
        self.base_size: QSize | None = None

    # 重写抽象类的方法, 实现具体功能
    # 加载器会在主体加载完成后调用这个方法
    def setupUi(self):
        self.widget = QWidget(self._parent)

        self.Label = QLabel(self.widget)
        self.Label.setText(("Hello World!\n" * 3)[:-1])

    # 加载器调用这个方法来获取主控件
    def getMainWidget(self):
        return self.widget

    # 加载器将会调用这个方法, 并将返回值作为页面名称
    def getTagName(self):
        return "Hello World Page"

    # 当父控件大小改变时, 会调用这个方法, 用于调整子控件大小
    def ReScale(self, x_scale: float, y_scale: float):
        x = (self._parent.width() - self.Label.width()) // 2
        y = (self._parent.height() - self.Label.height()) // 2

        # 将Label居中
        self.Label.move(
            x,
            y,
        )

    # 返回的值越小 页面越靠前
    @staticmethod
    def priority():
        return float("-inf")


# 将这个类注册到界面加载器中
register(HelloWorld)
