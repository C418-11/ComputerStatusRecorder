# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

import importlib
import os.path

from Lib.Configs import read_default_yaml, BASE_PATH

DefaultFeatures = read_default_yaml(
    os.path.join(BASE_PATH, "DefaultFeatures.yaml"),
    {
        "NetWorkTraffic": True,
        "Opacity": True,
    }
)


def load_default_features():
    def _load(name):
        if not DefaultFeatures[name]:
            return None

        print("loading feature:", name)
        return importlib.import_module("DefaultFeatures." + name)

    loaded_features = {}
    for feature in DefaultFeatures:
        loaded_features[feature] = _load(feature)

    return loaded_features


__all__ = ("DefaultFeatures", "load_default_features",)
