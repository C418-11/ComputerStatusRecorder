# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.2Dev"

import os
import struct
import time
import warnings
from enum import StrEnum


class PackFmt(StrEnum):
    Char = 'c'
    SignedChar = 'b'
    UnsignedChar = 'B'
    Bool = '?'
    Short = 'h'
    UnsignedShort = 'H'
    Int = 'i'
    UnsignedInt = 'I'
    Long = 'l'
    UnsignedLong = 'L'
    LongLong = 'q'
    UnsignedLongLong = 'Q'
    HalfFloat = 'e'
    Float = 'f'
    Double = 'd'


def pack_timestamp_que(que, *fmt_tuple, warn: bool = True):
    """
    :param que: queue[time.time_ns(), value]
    :param fmt_tuple: Iterable[PackFmt | str | "fmt1 fmt2 fmt3"]]
    :param warn: 是否警告非标准格式
    :return:
    """

    return pack_list(
        que,
        PackFmt.UnsignedLongLong,
        *fmt_tuple,
        warn=warn
    )


def pack_list(_list, *fmt_tuple, warn: bool = True):
    """
    :param _list: list[...]
    :param fmt_tuple: Iterable[PackFmt | str | "fmt1 fmt2 fmt3"]]
    :param warn: 是否警告非标准格式
    :return:
    """

    def _parse_fmt(_tuple):
        if len(_tuple) == 1:
            _fmt = _tuple[0]
            if type(_fmt) is str:
                return [_fmt]

        return [_f.value if type(_f) is PackFmt else _f for _f in fmt_tuple]

    fmt_ls: list[str] = _parse_fmt(fmt_tuple)

    for _ in fmt_ls:
        if _ not in PackFmt and warn:
            warnings.warn(
                f"fmt {_} is not in PackFmt",
                RuntimeWarning,
                stacklevel=2
            )

    file_head = b'|'.join([_.encode() for _ in fmt_ls]) + b'\n'  # 文件头记录文件解码格式
    ret_ls = [file_head]

    for value in _list:
        byte = b''
        for fmt, v in zip(fmt_ls, value):
            byte += struct.pack(fmt, v)

        ret_ls.append(byte)

    return ret_ls


def time_str(fmt, timestamp: int):
    return time.strftime(fmt, time.localtime(timestamp / 1000000000))


def mkdir(path: str, exist_ok=True):
    os.makedirs(path, exist_ok=exist_ok)


__all__ = ("PackFmt", "pack_timestamp_que", "time_str", "mkdir")
