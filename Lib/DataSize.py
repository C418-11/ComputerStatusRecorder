# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.2Dev"

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

    def __repr__(self):
        return f"<{self.fullname} ({self.abbreviation})>"

    def __str__(self):
        return repr(self)


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

unit_list: list[type[DataUnit]] = []

_ = YottaByte
while _:
    unit_list.append(_)
    try:
        _ = _.__base_unit__
    except AttributeError:
        break


def convert_to_base_unit(value: Decimal, data_unit: type[DataUnit]) -> tuple[Decimal, type[DataUnit]]:
    """
    转换为小一级单位
    """

    return value * data_unit.__base_conversion__, data_unit.__base_unit__


def convert_to_larger_unit(value: Decimal, data_unit: type[DataUnit]) -> tuple[Decimal, type[DataUnit]]:
    """
    转换为大一级单位
    """

    return value / data_unit.__larger_unit__.__base_conversion__, data_unit.__larger_unit__


def convert_to_base(
        value: Decimal,
        data_unit: type[DataUnit],
        target_unit: type[DataUnit],
) -> tuple[Decimal, type[DataUnit]]:
    """
    一直往小了尝试直到转换为目标单位
    """

    if data_unit is target_unit:
        return value, data_unit

    if not hasattr(data_unit, "__base_unit__"):
        raise ValueError("Cannot convert to smaller unit")

    else:
        v, u = convert_to_base_unit(value, data_unit)
        return convert_to_base(v, u, target_unit)


def convert_to_larger(
        value: Decimal,
        data_unit: type[DataUnit],
        target_unit: type[DataUnit]
) -> tuple[Decimal, type[DataUnit]]:
    """
    一直往大了尝试直到转换为目标单位
    """

    if data_unit is target_unit:
        return value, data_unit

    if not hasattr(data_unit, "__larger_unit__"):
        raise ValueError("Cannot convert to larger unit")

    else:
        v, u = convert_to_larger_unit(value, data_unit)
        return convert_to_larger(v, u, target_unit)


class CompareUnit(StrEnum):
    Larger = "larger"
    Lower = "lower"


def convert_to_best_unit(
        value: Decimal,
        unit: type[DataUnit],
        cmp=lambda v: CompareUnit.Larger if v > 1 else CompareUnit.Lower
) -> tuple[Decimal, type[DataUnit]]:
    """
    转换到最合适的单位
    """

    def _find(v, u, last_type, last_value=None, last_unit=None):
        if v == 1:
            return v, u

        now_type = cmp(v)

        if last_type is not None and now_type != last_type:
            return last_value, last_unit

        if now_type == CompareUnit.Lower:
            try:
                return _find(*convert_to_base_unit(v, u), now_type, v, u)
            except AttributeError:
                return v, u

        elif now_type == CompareUnit.Larger:
            try:
                return _find(*convert_to_larger_unit(v, u), now_type, v, u)
            except AttributeError:
                return v, u
        else:
            raise ValueError(f"Unknown type {now_type}")

    return _find(value, unit, None)


def convert_to_unit(
        value: Decimal,
        unit: type[DataUnit],
        target_unit: type[DataUnit]
) -> tuple[Decimal, type[DataUnit]]:
    """
    转换到目标单位
    """

    if unit == target_unit:
        return value, unit

    now = unit_list.index(unit)
    target = unit_list.index(target_unit)

    cmp = CompareUnit.Larger if now > target else CompareUnit.Lower

    result = None
    if cmp == CompareUnit.Larger:
        result = convert_to_larger(value, unit, target_unit)
    elif cmp == CompareUnit.Lower:
        result = convert_to_base(value, unit, target_unit)

    return result


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

    "unit_list",

    "convert_to_base_unit",
    "convert_to_larger_unit",

    "convert_to_base",
    "convert_to_larger",

    "convert_to_best_unit",
    "convert_to_unit",
)
