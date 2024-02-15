# -*- coding: utf-8 -*-
# cython: language_level = 3


widgets = set()


def register(widget):
    widgets.add(widget)


__all__ = ("widgets", "register",)
