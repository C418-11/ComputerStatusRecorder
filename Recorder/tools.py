# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

import struct

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


def time_str(fmt, timestamp: int | float):
    return time.strftime(fmt, time.localtime(timestamp))


__all__ = ("pack_timestamp_que", "time_str")
