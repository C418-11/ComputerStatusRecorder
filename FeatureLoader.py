# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.2Dev"

import importlib
import os.path
import sys

from Lib.Configs import read_default_yaml, BASE_PATH

DefaultFeatures = read_default_yaml(
    os.path.join(BASE_PATH, "DefaultFeatures.yaml"),
    {
        "NetWorkTraffic": True,
        "Opacity": True,
    }
)


def load_default_features():
    lib_path = os.path.join(os.path.dirname(__file__), "DefaultFeatures")
    sys.path.append(lib_path)

    def _load(name):
        if not bool(DefaultFeatures[name]):
            return None

        print("loading feature:", name)
        try:
            return importlib.import_module("DefaultFeatures." + name)
        except ImportError as err:
            print("feature load failed:", name, " reason:", err)
            return None

    loaded_features = {}
    for feature in DefaultFeatures:
        loaded_features[feature] = _load(feature)

    return loaded_features


OtherFeatures = read_default_yaml(
    os.path.join(BASE_PATH, "OtherFeatures.yaml"),
    {
        "YourFeatureName": "Is Enabled (true | false)",
        "HelloWorld": False
    }
)


def load_other_features():
    lib_path = os.path.join(os.path.dirname(__file__), "OtherFeatures")
    sys.path.append(lib_path)

    def _load(name):
        if name == "YourFeatureName":
            print("YourFeatureName is a reserved keyword, please change it to another name.")
            return None

        if not bool(OtherFeatures[name]):
            return None

        print("loading feature:", name)
        try:
            return importlib.import_module("Features." + name)
        except ImportError as err:
            print("feature load failed:", name, " reason:", err)
            return None

    loaded_features = {}
    for feature in OtherFeatures:
        loaded_features[feature] = _load(feature)

    return loaded_features


__all__ = ("DefaultFeatures", "load_default_features",)
