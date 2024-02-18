# -*- coding: utf-8 -*-
# cython: language_level = 3


from abc import ABC, abstractmethod


class ABCRecorder(ABC):
    def __init__(self, max_record_len: int, save_path: str):
        self.max_record_len: int = max_record_len
        self.save_path = save_path

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def save(self):
        ...


__all__ = ("ABCRecorder",)
