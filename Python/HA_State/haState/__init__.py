'''Base module level functions.'''

from typing import Any


class GlobalNamespace:

    __state: dict[str, Any] = {}

    def __init__(self, **kwargs):
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                self.__state[k] = v

        self.__dict__ = self.__state

    def __getattr__(self, attr: str) -> Any:
        if attr not in self.__dict__:
            raise TypeError(f'{attr} is not in the global namespace scope!')

        return self.__dict__[attr]
