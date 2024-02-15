# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

from abc import ABC
from decimal import Decimal
from enum import StrEnum
from typing import Self


class DataUnit(ABC):
    abbreviation: str
    fullname: str

    __base_unit__: type[Self]

    __base_conversion__: Decimal

    __larger_unit__: type[Self]


class Bit(DataUnit):
    abbreviation = "b"
    fullname = "Bit"


class Byte(DataUnit):
    abbreviation = "B"
    fullname = "Byte"

    __base_unit__ = Bit
    __base_conversion__ = Decimal(8)


Bit.__larger_unit__ = Byte


class KiloByte(DataUnit):
    abbreviation = "KB"
    fullname = "KiloByte"

    __base_unit__ = Byte
    __base_conversion__ = Decimal(1024)


Byte.__larger_unit__ = KiloByte


class MegaByte(DataUnit):
    abbreviation = "MB"
    fullname = "MegaByte"

    __base_unit__ = KiloByte
    __base_conversion__ = Decimal(1024)


KiloByte.__larger_unit__ = MegaByte


class GigaByte(DataUnit):
    abbreviation = "GB"
    fullname = "GigaByte"

    __base_unit__ = MegaByte
    __base_conversion__ = Decimal(1024)


MegaByte.__larger_unit__ = GigaByte


class TeraByte(DataUnit):
    abbreviation = "TB"
    fullname = "TeraByte"

    __base_unit__ = GigaByte
    __base_conversion__ = Decimal(1024)


GigaByte.__larger_unit__ = TeraByte


class PetaByte(DataUnit):
    abbreviation = "PB"
    fullname = "PetaByte"

    __base_unit__ = TeraByte
    __base_conversion__ = Decimal(1024)


TeraByte.__larger_unit__ = PetaByte


class ExaByte(DataUnit):
    abbreviation = "EB"
    fullname = "ExaByte"

    __base_unit__ = PetaByte
    __base_conversion__ = Decimal(1024)


PetaByte.__larger_unit__ = ExaByte


class ZettaByte(DataUnit):
    abbreviation = "ZB"
    fullname = "ZettaByte"

    __base_unit__ = ExaByte
    __base_conversion__ = Decimal(1024)


ExaByte.__larger_unit__ = ZettaByte


class YottaByte(DataUnit):
    abbreviation = "YB"
    fullname = "YottaByte"

    __base_unit__ = ZettaByte
    __base_conversion__ = Decimal(1024)


ZettaByte.__larger_unit__ = YottaByte


def _convert_to_base_unit(value: Decimal, data_unit: type[DataUnit]) -> tuple[Decimal, type[DataUnit]]:
    return value * data_unit.__base_conversion__, data_unit.__base_unit__


def _convert_to_larger_unit(value: Decimal, data_unit: type[DataUnit]) -> tuple[Decimal, type[DataUnit]]:
    return value / data_unit.__larger_unit__.__base_conversion__, data_unit.__larger_unit__


def _convert_to_base(
        value: Decimal,
        data_unit: type[DataUnit],
        target_unit: type[DataUnit],
) -> tuple[Decimal, type[DataUnit]]:
    if not hasattr(data_unit, "__base_unit__"):
        return value, data_unit
    if data_unit is target_unit:
        return value, data_unit

    else:
        return _convert_to_base(*_convert_to_base_unit(value, data_unit))


def _convert_to_larger(
        value: Decimal,
        data_unit: type[DataUnit],
        target_unit: type[DataUnit]
) -> tuple[Decimal, type[DataUnit]]:
    if not hasattr(data_unit, "__larger_unit__"):
        return value, data_unit

    if data_unit.__larger_unit__ is target_unit:
        return value, data_unit

    else:
        return _convert_to_larger(*_convert_to_larger_unit(value, data_unit))


def convert_to_best_unit(value: Decimal, unit: type[DataUnit]) -> tuple[Decimal, DataUnit]:
    class LastType(StrEnum):
        Larger = "larger"
        Lower = "lower"

    def _find(v, u, last_type, last_value=None, last_unit=None):
        if v == 1:
            return v, u

        now_type = LastType.Lower if v < 1 else LastType.Larger

        if last_type is not None and now_type != last_type:
            return last_value, last_unit

        if now_type == LastType.Lower:
            try:
                return _find(*_convert_to_base_unit(v, u), now_type, v, u)
            except AttributeError:
                return v, u

        elif now_type == LastType.Larger:
            try:
                return _find(*_convert_to_larger_unit(v, u), now_type, v, u)
            except AttributeError:
                return v, u
        else:
            raise ValueError(f"Unknown type {now_type}")

    return _find(value, unit, None)


if __name__ == "__main__":
    print(convert_to_best_unit(Decimal(8 * 1024 ** 9), Bit))

__all__ = (
    "DataUnit",

    "Bit",
    "Byte",
    "KiloByte",
    "MegaByte",
    "GigaByte",
    "TeraByte",
    "PetaByte",
    "ExaByte",
    "ZettaByte",
    "YottaByte",

    "convert_to_best_unit"
)
