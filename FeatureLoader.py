# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.3Dev"

import importlib
import os.path
import re
import sys

from Lib.Configs import read_default_yaml, BASE_PATH

DefaultFeatures = read_default_yaml(
    os.path.join(BASE_PATH, "DefaultFeatures.yaml"),
    {
        "1|NetWorkTraffic": True,  # 这里的 '|' 是为了保证写入顺序 (实测发现yaml写入顺序与dict不一致, 疑似做了排序)
        "2|Memory": True,  # 这里保证写入顺序的主要原因是加载顺序敏感, 会导致界面的显示顺序不一致
        "3|WindowTop": True,
        "4|Opacity": True,
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

        if err_module == import_path:
            print("Feature not found:", f"{import_path}.{name}")
            return None

        if err_module == f"{import_path}.{name}":
            print("Feature not found:", name)
            return None

        print(f"Unable to load Feature '{name}', dependencies may not be installed: '{err_module}'")
        return None
    except Exception as err:
        print("Unable to load Feature:", name, " reason:", err)
        return None


def _get_details(module):
    detail_dict = {}

    for attr in ("__author__", "__description__", "__version__"):
        value = getattr(module, attr, None)

        if value is not None:
            detail_dict[attr] = value

    return detail_dict


def _show_details(module):
    details = _get_details(module)

    if not details:
        print("  No details available")
        return

    key_map = {
        "__author__": "Auther",
        "__description__": "Desc",
        "__version__": "Ver"
    }

    for attr, value in details.items():
        print(f"  {key_map[attr]}: {value}")


def load_default_features():
    lib_path = os.path.join(os.path.dirname(__file__), "DefaultFeatures")
    sys.path.append(lib_path)

    loaded_features = {}
    for feature in DefaultFeatures:
        if not bool(DefaultFeatures[feature]):
            print("Feature disabled:", feature)
            loaded_features[feature] = None
            continue
        if '|' in feature:
            feature = feature.split('|')[1]
        loaded_features[feature] = _load(feature, "DefaultFeatures")

        _show_details(loaded_features[feature])

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

        _show_details(loaded_features[feature])

    return loaded_features


__all__ = ("DefaultFeatures", "load_default_features",)
