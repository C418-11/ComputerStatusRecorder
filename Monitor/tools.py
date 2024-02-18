# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

import functools


def update_check(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.update_when_getter:
            self.update_data()

        return func(self, *args, **kwargs)

    return wrapper


def dont_update_during_running(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        old = self.update_when_getter
        self.update_when_getter = False
        ret = func(self, *args, **kwargs)
        self.update_when_getter = old

        return ret

    return wrapper


__all__ = ("update_check", "dont_update_during_running",)
