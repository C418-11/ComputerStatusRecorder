# -*- coding: utf-8 -*-
# cython: language_level = 3

from typing import override

import psutil

from Monitor.ABC import ABCMonitor
from Monitor.tools import update_check


class Memory(ABCMonitor):
    total: int | None
    used: int | None
    free: int | None
    available: int | None
    percent: float | None

    def __init__(self):
        self._v_total: int | None = None
        self._v_used: int | None = None
        self._v_free: int | None = None
        self._v_available: int | None = None
        self._v_percent: float | None = None

    @override
    def update_data(self):
        self._v_total = psutil.virtual_memory().total
        self._v_used = psutil.virtual_memory().used
        self._v_free = psutil.virtual_memory().free
        self._v_available = psutil.virtual_memory().available
        self._v_percent = psutil.virtual_memory().percent

    @update_check
    @override
    def __getattr__(self, item):
        if item.startswith("_v_"):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
        return getattr(self, "_v_" + item)


__all__ = ("Memory",)
