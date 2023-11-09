from typing import Any
from main.cache_manager import CacheInterface


class UsernameCache(CacheInterface):
    def __init__(self) -> None:
        self.__cache = ()

    def get(self, value: Any) -> Any | None:
        if value in self.__cache:
            return value
        return None

    def set(self, value: Any) -> bool:
        if not self.get(value):
            self.__cache += (value,)
            return True
        return False

    def delete(self, value: Any) -> bool:
        new_cache = [*self.__cache]
        try:
            new_cache.remove(value)
        except ValueError:
            pass
        self.__cache = (*new_cache,)
        del new_cache
        return True

    def clear_cache(self) -> bool:
        self.__cache = ()
        return True
