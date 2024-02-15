# -*- coding: utf-8 -*-
# cython: language_level = 3


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
    def getMainWidget(self):
        ...

    @abstractmethod
    def getTagName(self):
        ...


class AbcMenu(ABC):
    def __init__(self, _parent: QMenuBar): ...

    @abstractmethod
    def setupUi(self):
        ...

    @abstractmethod
    def getMenuWidget(self):
        ...
