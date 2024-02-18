# -*- coding: utf-8 -*-
# cython: language_level = 3

import os
from decimal import Decimal
from enum import StrEnum
from typing import override

from Lib import DataSize
from Monitor.Memory import Memory as MMemory
from Recorder.ABC import ABCRecorder
from collections import deque
from Lib.DataSize import convert_to_best_unit, DataUnit
from Recorder.tools import pack_timestamp_que as _pack, PackFmt
from Recorder.tools import mkdir as _mkdir
from Recorder.tools import time_str as _time_str

import time


class PathType(StrEnum):
    TOTAL = "total"
    USED = "used"
    FREE = "free"
    AVAILABLE = "available"
    PERCENT = "percent"


class Memory(ABCRecorder):
    total: int
    used: int
    free: int
    available: int
    percent: float

    def __init__(self, max_record_len: int = 60, save_path: str = "./"):
        super().__init__(max_record_len, save_path)

        self.getter = MMemory()
        self.getter.update_when_getter = False

        self.start_time: int | None = None

        self.total_que = deque(maxlen=self.max_record_len)
        self.used_que = deque(maxlen=self.max_record_len)
        self.free_que = deque(maxlen=self.max_record_len)
        self.available_que = deque(maxlen=self.max_record_len)
        self.percent_que = deque(maxlen=self.max_record_len)

        self.total_unit: tuple[Decimal, DataUnit] | None = None
        self.used_unit: tuple[Decimal, DataUnit] | None = None
        self.free_unit: tuple[Decimal, DataUnit] | None = None
        self.available_unit: tuple[Decimal, DataUnit] | None = None

    @override
    def update(self):
        if self.start_time is None:
            self.start_time = time.time_ns()

        self.getter.update_data()
        get_at = time.time_ns()

        self.total_que.append((get_at, self.getter.total))
        self.used_que.append((get_at, self.getter.used))
        self.free_que.append((get_at, self.getter.free))
        self.available_que.append((get_at, self.getter.available))
        self.percent_que.append((get_at, self.getter.percent))

        self.total_unit = convert_to_best_unit(Decimal(self.getter.total), DataSize.Byte)
        self.used_unit = convert_to_best_unit(Decimal(self.getter.used), DataSize.Byte)
        self.free_unit = convert_to_best_unit(Decimal(self.getter.free), DataSize.Byte)
        self.available_unit = convert_to_best_unit(Decimal(self.getter.available), DataSize.Byte)

    @override
    def save(self) -> dict[PathType, str]:
        start_str = _time_str("%Y-%m-%d--%H-%M-%S", self.start_time)
        finish_str = _time_str("%Y-%m-%d--%H-%M-%S", time.time_ns())

        def _write(que: deque, type_, fmt: PackFmt = PackFmt.Int):
            life = f"Time[Start[{start_str}],Finish[{finish_str}]]"
            type_str = f"Type[{type_}]"
            ext = ".MemoryRecord"

            data_path = os.path.join(self.save_path, ".MemoryRecord")
            _mkdir(data_path)

            with open(os.path.join(data_path, f"{life},{type_str}{ext}"), 'ab') as file:
                for b in _pack(que, fmt=fmt):
                    file.write(b)

            return os.path.abspath(os.path.join(data_path, f"{life},{type_str}{ext}"))

        type_ls = {
            PathType.TOTAL: self.total_que,
            PathType.USED: self.used_que,
            PathType.FREE: self.free_que,
            PathType.AVAILABLE: self.available_que,
        }

        ret_dict = {type_: _write(que, type_) for type_, que in type_ls.items()}
        ret_dict[PathType.PERCENT] = _write(self.percent_que, PathType.PERCENT, PackFmt.Float)

        return ret_dict

    def __getattr__(self, item):
        return self.getter.__getattr__(item)


__all__ = ("PathType", "Memory",)
