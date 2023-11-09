from typing import Any
from .interfaces import CacheManagerInterface, CacheInterface
from pympler.asizeof import asizeof


class CacheManager(CacheManagerInterface):
    def __init__(
        self, max_memory_cache: int, caches: dict[str, CacheInterface]
    ) -> None:
        self.__MAX_MEMORY_CACHE = max_memory_cache * 1000000  # Convert to bytes
        self.__caches_class = caches
        self.__CACHE_MEMORY_DIVIDE = self.__MAX_MEMORY_CACHE / len(self.__caches_class)

    def private__verify_cache_size(self, cache_name: str) -> bool:
        if asizeof(self.__caches_class[cache_name]) >= self.__CACHE_MEMORY_DIVIDE:
            print(f"{cache_name} clear cache")
            self.__caches_class[cache_name].clear_cache()

    def get(self, cache_name: str, value: Any) -> Any | None:
        value_return = self.__caches_class[cache_name].get(value)
        self.private__verify_cache_size(cache_name)
        return value_return

    def set(self, cache_name: str, value: Any) -> bool:
        value_return = self.__caches_class[cache_name].set(value)
        self.private__verify_cache_size(cache_name)
        return value_return

    def delete(self, cache_name: str, value: Any) -> bool:
        value_return = self.__caches_class[cache_name].delete(value)
        self.private__verify_cache_size(cache_name)
        return value_return
