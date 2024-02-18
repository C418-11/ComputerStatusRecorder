# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"


from abc import ABC, abstractmethod


class ABCMonitor(ABC):
    update_when_getter: bool = False

    @abstractmethod
    def update_data(self):
        ...

    @abstractmethod
    def __getattr__(self, item):
        ...


__all__ = ("ABCMonitor",)
