from abc import ABC, abstractmethod
from typing import Union, Any

from .cache_interface import CacheInterface


class CacheManagerInterface(ABC):
    @abstractmethod
    def __init__(
        self, max_memory_cache: int, caches: dict[str, CacheInterface]
    ) -> None:
        """Cache manager

        Args:
            max_memory_cache (int): Max memory used by cache class, in MB
            caches (dict[str, CacheInterface]): Caches classes to verify cache
        """
        raise NotImplementedError()

    @abstractmethod
    def get(self, cache_name: str, value: Any) -> Union[Any, None]:
        """Get the value if exists in cache

        Args:
            cache_name (str): cache class name
            value (Any): value

        Returns:
            Union[Any, None]: Return the value or None if not exists
        """
        raise NotImplementedError()

    @abstractmethod
    def set(self, cache_name: str, value: Any) -> bool:
        """Set the value in cache

        Args:
            cache_name (str): cache class name
            value (Any): value

        Returns:
            bool: True if success, False if not
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, cache_name: str, value: Any) -> bool:
        """Delete the value in cache

        Args:
            cache_name (str): cache class name
            value (Any): value

        Returns:
            bool: True if success, False if not
        """
        raise NotImplementedError()
