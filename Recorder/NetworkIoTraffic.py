# -*- coding: utf-8 -*-
# cython: language_level = 3

import os.path
import time
from collections import deque
from decimal import Decimal
from typing import override

from Lib import DataSize
from Lib.DataSize import convert_to_best_unit
from Monitor.NetIoCounter import NetIoCounter
from Recorder.ABC import ABCRecorder
from Recorder.tools import PackFmt
from Recorder.tools import mkdir as _mkdir
from Recorder.tools import pack_timestamp_que as _pack
from Recorder.tools import time_str as _time_str


class NetIoTraffic(ABCRecorder):
    def __init__(self, max_record_len=60, save_path="./"):
        super().__init__(max_record_len=max_record_len, save_path=save_path)
        self.bytes_getter = NetIoCounter()
        self.bytes_getter.update_when_getter = False

        self.this_sent_que = deque(maxlen=self.max_record_len)
        self.this_recv_que = deque(maxlen=self.max_record_len)

        self.start_time: int | None = None

        self.last_sent = None
        self.last_recv = None

        self.this_sent = None
        self.this_recv = None

        self.sent_unit = None
        self.recv_unit = None

    def _update_this_bytes(self, get_at: int):
        if self.start_time is None:
            self.start_time = time.time_ns()

        b_sent = self.bytes_getter.bytes_sent
        b_recv = self.bytes_getter.bytes_recv

        self.this_sent = b_sent - (self.last_sent if self.last_sent else b_sent)
        self.this_recv = b_recv - (self.last_recv if self.last_recv else b_recv)

        self.last_sent = b_sent
        self.last_recv = b_recv

        self.this_sent_que.append((get_at, self.this_sent))
        self.this_recv_que.append((get_at, self.this_recv))

    @override
    def update(self):
        self.bytes_getter.update_data()
        self._update_this_bytes(time.time_ns())

        self.sent_unit = convert_to_best_unit(Decimal(self.this_sent), DataSize.Byte)
        self.recv_unit = convert_to_best_unit(Decimal(self.this_recv), DataSize.Byte)

    @override
    def save(self):
        start_str = _time_str("%Y-%m-%d--%H-%M-%S", self.start_time)
        finish_str = _time_str("%Y-%m-%d--%H-%M-%S", time.time_ns())

        def _write(que: deque, type_):
            life = f"Time[Start[{start_str}],Finish[{finish_str}]]"
            type_str = f"Type[{type_}]"
            ext = ".NetworkIoRecord"

            data_path = os.path.join(self.save_path, ".NetworkIoRecord")
            _mkdir(data_path)

            with open(os.path.join(data_path, f"{life},{type_str}{ext}"), 'ab') as file:
                for b in _pack(que, PackFmt.UnsignedLongLong):
                    file.write(b)

            return os.path.abspath(os.path.join(data_path, f"{life},{type_str}{ext}"))

        return _write(self.this_sent_que, "Sent"), _write(self.this_recv_que, "Recv")
