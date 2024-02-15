# -*- coding: utf-8 -*-
# cython: language_level = 3

import functools
from enum import StrEnum

import psutil


def _update_check(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.update_when_getter:
            self.update_data()

        return func(self, *args, **kwargs)

    return wrapper


def _dont_update_during_running(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        old = self.update_when_getter
        self.update_when_getter = False
        ret = func(self, *args, **kwargs)
        self.update_when_getter = old

        return ret

    return wrapper


class CounterMode(StrEnum):
    TOTAL = "total"
    EVERY = "every"


class NetIoCounter:
    reader = functools.partial(psutil.net_io_counters, pernic=False)

    bytes_recv: int | dict[str, int]
    bytes_sent: int | dict[str, int]

    packets_recv: int | dict[str, int]
    packets_sent: int | dict[str, int]

    drop_in: int | dict[str, int]
    drop_out: int | dict[str, int]

    err_in: int | dict[str, int]
    err_out: int | dict[str, int]

    def __init__(self, mode: CounterMode = CounterMode.TOTAL):
        self.mode = CounterMode(mode)

        self.update_when_getter = False

        self._bytes_recv = None
        self._bytes_sent = None

        self._packets_recv = None
        self._packets_sent = None

        self._drop_in = None
        self._drop_out = None

        self._err_in = None
        self._err_out = None

    def update_data(self):
        net_io = self.reader()

        if self.mode == CounterMode.TOTAL:
            bytes_recv = net_io.bytes_recv
            bytes_sent = net_io.bytes_sent

            packets_recv = net_io.packets_recv
            packets_sent = net_io.packets_sent

            drop_in = net_io.dropin
            drop_out = net_io.dropout

            err_in = net_io.errout
            err_out = net_io.errout

        elif self.mode == CounterMode.EVERY:
            if type(net_io) is not dict:
                raise ValueError(f"net_io must be a dict when mode is '{CounterMode.EVERY}'")

            def _all(attr):
                return {k: getattr(v, attr) for k, v in net_io.items()}

            bytes_recv = _all("bytes_recv")
            bytes_sent = _all("bytes_sent")

            packets_recv = _all("packets_recv")
            packets_sent = _all("packets_sent")

            drop_in = _all("dropin")
            drop_out = _all("dropout")

            err_in = _all("errout")
            err_out = _all("errout")

        else:
            raise ValueError("Unknown counter mode")

        self._bytes_recv = bytes_recv
        self._bytes_sent = bytes_sent

        self._packets_recv = packets_recv
        self._packets_sent = packets_sent

        self._drop_in = drop_in
        self._drop_out = drop_out

        self._err_in = err_in
        self._err_out = err_out

    # 当读取属性时，自动更新数据
    @_update_check
    def __getattr__(self, item):
        return getattr(self, "_" + item)


__all__ = ("NetIoCounter", "CounterMode")
