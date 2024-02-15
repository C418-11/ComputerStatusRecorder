# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

import os.path
import struct
import time
from collections import deque
from decimal import Decimal

from Lib import DataSize
from Lib.DataSize import convert_to_best_unit
from Monitor.NetIoCounter import NetIoCounter


def _mkdir(path: str):
    # 尝试一次性创建多级目录
    os.makedirs(path, exist_ok=True)


def _pack(que: deque) -> list[bytes]:
    def _int_timestamp(t: Decimal) -> Decimal:
        float_long = len(str(t - int(t)))
        return t * (10 ** float_long)

    ls = []

    for timestamp, value in que:
        byte = struct.pack('Q', int(_int_timestamp(Decimal(str(timestamp)))))
        byte += struct.pack('Q', int(value))
        ls.append(byte)

    return ls


class NetIoTraffic:
    def __init__(self, max_record_len=1 * 60 * 60, file_path="./"):
        self.bytes_getter = NetIoCounter()
        self.bytes_getter.update_when_getter = False

        self.file_path = file_path

        self.this_sent_que = deque(maxlen=max_record_len)
        self.this_recv_que = deque(maxlen=max_record_len)

        self.start_time = time.time()

        self.last_sent = None
        self.last_recv = None

        self.this_sent = None
        self.this_recv = None

        self.sent_unit = None
        self.recv_unit = None

    def _update_this_bytes(self):
        if self.start_time is None:
            self.start_time = time.time()

        b_sent = self.bytes_getter.bytes_sent
        b_recv = self.bytes_getter.bytes_recv

        self.this_sent = b_sent - (self.last_sent if self.last_sent else b_sent)
        self.this_recv = b_recv - (self.last_recv if self.last_recv else b_recv)

        self.last_sent = b_sent
        self.last_recv = b_recv

        self.this_sent_que.append((time.time(), self.this_sent))
        self.this_recv_que.append((time.time(), self.this_recv))

    def update(self):
        self.bytes_getter.update_data()
        self._update_this_bytes()

        self.sent_unit = convert_to_best_unit(Decimal(self.this_sent), DataSize.Byte)
        self.recv_unit = convert_to_best_unit(Decimal(self.this_recv), DataSize.Byte)

    def save(self):
        time_str = time.strftime("%Y-%m-%d--%H-%M-%S", time.localtime(self.start_time))
        finish_str = time.strftime("%Y-%m-%d--%H-%M-%S", time.localtime(time.time()))

        def _write(que: deque, type_):
            life = f"Time[Start[{time_str}],Finish[{finish_str}]]"
            type_str = f"Type[{type_}]"
            ext = ".NetworkIoRecord"

            data_path = os.path.join(self.file_path, ".NetworkIoRecord")
            _mkdir(data_path)

            with open(os.path.join(data_path, f"{life},{type_str}{ext}"), 'ab') as file:
                for b in _pack(que):
                    file.write(b)

            return os.path.abspath(os.path.join(data_path, f"{life},{type_str}{ext}"))

        return _write(self.this_sent_que, "Sent"), _write(self.this_recv_que, "Recv")
