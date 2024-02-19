# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

import os
import struct
import time
from enum import StrEnum


class PackFmt(StrEnum):
    Int = 'Q'
    Float = 'd'


def pack_timestamp_que(que, fmt=PackFmt.Int):
    """
    :param que: queue[time.time_ns(), value]
    :param fmt: struct.pack(fmt, value)
    :return:
    """

    if not isinstance(fmt, PackFmt):
        raise TypeError("fmt must be PackFmt")

    ls = []

    for timestamp, value in que:

        if type(timestamp) is not int:
            raise TypeError("timestamp must be int")

        byte = struct.pack('Q', timestamp)
        byte += struct.pack(fmt, value)
        ls.append(byte)

    return ls


def time_str(fmt, timestamp: int):
    return time.strftime(fmt, time.localtime(timestamp / 1000000000))


def mkdir(path: str, exist_ok=True):
    os.makedirs(path, exist_ok=exist_ok)


__all__ = ("PackFmt", "pack_timestamp_que", "time_str", "mkdir")
