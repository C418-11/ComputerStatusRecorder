# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

import os
import struct
from decimal import Decimal
import time


def pack_timestamp_que(que):
    """
    :param que: queue[time.time_ns(), value]
    :return:
    """

    ls = []

    for timestamp, value in que:

        if type(timestamp) is not int:
            raise TypeError("timestamp must be int")

        if type(value) is not int:
            raise TypeError("value must be int")

        byte = struct.pack('Q', timestamp)
        byte += struct.pack('Q', value)
        ls.append(byte)

    return ls


def time_str(fmt, timestamp: int):
    timestamp = Decimal(timestamp) / Decimal(1000000000)
    return time.strftime(fmt, time.localtime(float(timestamp)))


def mkdir(path: str, exist_ok=True):
    os.makedirs(path, exist_ok=exist_ok)


__all__ = ("pack_timestamp_que", "time_str", "mkdir")
