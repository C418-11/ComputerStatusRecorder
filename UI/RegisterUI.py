# -*- coding: utf-8 -*-
# cython: language_level = 3


__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.2Dev"

from UI.ABC import AbcUI, AbcMenu

widgets: set[type[AbcUI]] = set()


def register(widget: type[AbcUI]):
    widgets.add(widget)


menu: set[type[AbcMenu]] = set()


def register_menu(menu_item: type[AbcMenu]):
    menu.add(menu_item)


__all__ = ("widgets", "register", "menu", "register_menu",)
