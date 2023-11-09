from abc import ABC, abstractmethod
from typing import Union, Any


class CacheInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        """Cache class"""
        raise NotImplementedError()

    @abstractmethod
    def get(self, value: Any) -> Union[Any, None]:
        """Get the value if exists in cache

        Args:
            value (Any): value

        Returns:
            Union[Any, None]: Return the value or None if not exists
        """
        raise NotImplementedError()

    @abstractmethod
    def set(self, value: Any) -> bool:
        """Set the value in cache

        Args:
            value (Any): value

        Returns:
            bool: True if success, False if not
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, value: Any) -> bool:
        """Set the value in cache

        Args:
            value (Any): value

        Returns:
            bool: True if success, False if not
        """
        raise NotImplementedError()

    @abstractmethod
    def clear_cache(self) -> bool:
        """Clear cache

        Returns:
            bool: True if success, False if not
        """
        raise NotImplementedError()
