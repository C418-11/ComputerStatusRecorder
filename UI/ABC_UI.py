# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"


from abc import ABC
from abc import abstractmethod
from PyQt5.QtWidgets import *


class AbcUI(ABC):
    def __init__(self, _parent: QTabWidget): ...

    def ReScale(self, x_scale: float, y_scale: float):
        ...

    @abstractmethod
    def setupUi(self):
        ...

    @abstractmethod
    def getItemWidget(self):
        ...

    @abstractmethod
    def getTagName(self):
        ...
