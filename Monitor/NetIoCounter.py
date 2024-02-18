# -*- coding: utf-8 -*-
# cython: language_level = 3

import functools
from enum import StrEnum
from typing import override

import psutil

from Monitor.ABC import ABCMonitor
from Monitor.tools import update_check


class CounterMode(StrEnum):
    TOTAL = "total"
    EVERY = "every"


class NetIoCounter(ABCMonitor):
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

        self._v_bytes_recv = None
        self._v_bytes_sent = None

        self._v_packets_recv = None
        self._v_packets_sent = None

        self._v_drop_in = None
        self._v_drop_out = None

        self._v_err_in = None
        self._v_err_out = None

    @override
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

        self._v_bytes_recv = bytes_recv
        self._v_bytes_sent = bytes_sent

        self._v_packets_recv = packets_recv
        self._v_packets_sent = packets_sent

        self._v_drop_in = drop_in
        self._v_drop_out = drop_out

        self._v_err_in = err_in
        self._v_err_out = err_out

    @update_check
    @override
    def __getattr__(self, item):
        return getattr(self, "_v_" + item)


__all__ = ("NetIoCounter", "CounterMode")
