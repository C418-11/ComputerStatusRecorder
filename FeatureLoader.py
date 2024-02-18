# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.2Dev"

import importlib
import os.path
import sys
import re

from Lib.Configs import read_default_yaml, BASE_PATH

DefaultFeatures = read_default_yaml(
    os.path.join(BASE_PATH, "DefaultFeatures.yaml"),
    {
        "NetWorkTraffic": True,
        "Opacity": True,
    }
)


def _load(name: str, import_path: str):
    try:
        module = importlib.import_module(f"{import_path}.{name}")
        print("Feature loaded successfully:", name)
        return module
    except ImportError as err:
        c = re.compile(r"No\smodule\snamed\s'([^']+)'")
        err_module = c.findall(str(err))

        if (not err_module) or len(err_module) != 1:
            print("Unable to load Feature:", name, " reason:", err)
            return None

        err_module = err_module[0]

        if err_module == f"{import_path}.{name}":
            print("Feature not found:", name)
            return None

        print(f"Unable to load Feature '{name}', dependencies may not be installed: '{err_module}'")
        return None
    except Exception as err:
        print("Unable to load Feature:", name, " reason:", err)
        return None


def load_default_features():
    lib_path = os.path.join(os.path.dirname(__file__), "DefaultFeatures")
    sys.path.append(lib_path)

    loaded_features = {}
    for feature in DefaultFeatures:
        if not bool(DefaultFeatures[feature]):
            print("Feature disabled:", feature)
            loaded_features[feature] = None
            continue

        loaded_features[feature] = _load(feature, "DefaultFeatures")

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

    loaded_features = {}
    for feature in OtherFeatures:
        if feature == "YourFeatureName":
            print("YourFeatureName is a reserved keyword, please change it to another name.")
            continue

        if not bool(OtherFeatures[feature]):
            print("Feature disabled:", feature)
            loaded_features[feature] = None
            continue

        loaded_features[feature] = _load(feature, "Features")

    return loaded_features


__all__ = ("DefaultFeatures", "load_default_features",)
