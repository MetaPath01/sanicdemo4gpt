import os
import sys
import shelve

from typing import (
    Any,
    Awaitable,
    ContextManager,
    Coroutine,
    Mapping,
    MutableMapping,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
    List
)


def is_in_shelve(shelve_dir: str, key: str):
    os.makedirs(shelve_dir, exist_ok=True)
    shelve_path = os.path.join(shelve_dir, 'data')
    d_shelve = shelve.open(shelve_path)
    out = key in d_shelve
    d_shelve.close()
    return out

def keys_in_shelve(shelve_dir: str):
    os.makedirs(shelve_dir, exist_ok=True)
    shelve_path = os.path.join(shelve_dir, 'data')
    d_shelve = shelve.open(shelve_path)
    key_l = list(d_shelve.keys())
    d_shelve.close()
    return key_l


def load_shelve(shelve_dir: str, key: str):
    os.makedirs(shelve_dir, exist_ok=True)
    shelve_path = os.path.join(shelve_dir, 'data')
    d_shelve = shelve.open(shelve_path)
    value = d_shelve[key]
    d_shelve.close()
    return value


def dump_shelve(shelve_dir: str, key: str, value: Any):
    os.makedirs(shelve_dir, exist_ok=True)
    shelve_path = os.path.join(shelve_dir, 'data')
    d_shelve = shelve.open(shelve_path)
    d_shelve[key] = value
    d_shelve.close()


def del_shelve(shelve_dir: str, key: str):
    os.makedirs(shelve_dir, exist_ok=True)
    shelve_path = os.path.join(shelve_dir, 'data')
    d_shelve = shelve.open(shelve_path)
    del d_shelve[key]
    d_shelve.close()


def update_shelve(shelve_dir: str, key: str, item: Any):
    if not is_in_shelve(shelve_dir, key):
        dump_shelve(shelve_dir, key, item)
        return item
    os.makedirs(shelve_dir, exist_ok=True)
    shelve_path = os.path.join(shelve_dir, 'data')
    d_shelve = shelve.open(shelve_path)
    value = d_shelve[key]
    if isinstance(value, list):
        if not isinstance(item, list):
            raise Exception(f"value and item type must be same")
        else:
            if len(set(value)) == len(value):
                value.extend(item)
                value = list(set(value))
            else:
                value.extend(item)
    elif isinstance(value, dict) and isinstance(item, dict):
        value.update(item)
    d_shelve[key] = value
    d_shelve.close()
    return value


class ContainShelve:
    def __init__(self, shelve_path: str, **kwargs: Any) -> None:
        self.__shelve_path = shelve_path
        super().__init__(**kwargs)

    def get_shelve_path(self) -> None:
        return self.__shelve_path

    def is_in_shelve(self, key: str) -> bool:
        return is_in_shelve(self.__shelve_path, key)

    def keys_in_shelve(self) -> List:
        return keys_in_shelve(self.__shelve_path)

    def load_shelve(self, key: str) -> Any:
        return load_shelve(self.__shelve_path, key)

    def dump_shelve(self, key: str, value: Any) -> None:
        dump_shelve(self.__shelve_path, key, value)

    def del_shelve(self, key: str) -> None:
        return del_shelve(self.__shelve_path, key)

    def update_shelve(self, key: str, item: Any) -> None:
        return update_shelve(self.__shelve_path, key, item)

    def __setitem__(self, key: str, value: Any):
        self.dump_shelve(key, value)

    def __getitem__(self, key: str):
        return self.load_shelve(key)

    def __contains__(self, key: str):
        return self.is_in_shelve(key)

    def keys(self):
        return self.keys_in_shelve()

    def __delitem__(self, key):
        self.del_shelve(key)

    def __len__(self):
        return len(self.keys())