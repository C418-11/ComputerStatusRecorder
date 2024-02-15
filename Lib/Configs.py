# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.2Dev"

import yaml

import os


def read_default_yaml(path: str, default_config):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            yaml.safe_dump(default_config, f)
    with open(path, 'r') as f:
        return Config(yaml.safe_load(f), file_path=path)


BASE_PATH = './.configs/'
if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)


class Config:
    def __init__(
            self,
            config,
            path_from_root: list | None = None,
            file_path: str | None = None
    ):
        if path_from_root is None:
            path_from_root = []

        self._config = config
        self._path_from_root = path_from_root
        self._file_path = file_path

        for key in config:
            if hasattr(self, key):
                raise KeyError(f"'{key}' is a reserved keyword")

    def get_default(self, key, default):
        if key in self:
            return self[key]
        return default

    @property
    def raw_config(self):
        return self._config

    def _key_not_found_message_box(self, key):
        path_str = ' -> '.join(self._path_from_root + [key])
        from tkinter import messagebox
        messagebox.showerror(
            "Error",
            f"Cannot find key {path_str} in configuration file {self._file_path}",
        )

    def keys(self):
        return self._config.keys()

    def __repr__(self):
        return f"<Config raw={self._config} path={self._path_from_root} file={self._file_path}>"

    def __iter__(self):
        return iter(self._config)

    def __contains__(self, item):
        return item in self._config

    def __getitem__(self, item):
        try:
            ret = self._config[item]
        except KeyError:
            self._key_not_found_message_box(item)
            raise
        else:
            if type(ret) is dict or type(ret) is list or type(ret) is tuple:
                ret = Config(ret, path_from_root=self._path_from_root + [item], file_path=self._file_path)

            return ret


_screen = read_default_yaml(os.path.join(BASE_PATH, 'Screen.yaml'), {
    "MinimumSize": {
        "width": 680,
        "height": 520
    }
})

try:
    MinimumSize = tuple(int(_screen["MinimumSize"][key]) for key in ("width", "height"))
except KeyError:
    MinimumSize = (680, 520)
