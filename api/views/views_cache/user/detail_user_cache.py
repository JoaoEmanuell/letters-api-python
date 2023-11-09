from typing import Any
from main.cache_manager import CacheInterface


class DetailUserCache(CacheInterface):
    def __init__(self) -> None:
        self.__cache = ()

    def get(self, value: Any) -> Any | None:
        """
        Args:
            value (str): user token
        """
        if value in self.__cache:
            user_index = self.__cache.index(value)
            return self.private__transform_user_tuple_in_dict(
                self.__cache[user_index + 1]
            )
        return None

    def set(self, value: Any) -> bool:
        """

        Args:
            value (dict): {user_token: "token", user_data: list[dict]}
        """
        user_token = value["user_token"]
        if not self.get(value):
            data = self.private__transform_user_dict_in_tuple(value["user_data"])
            try:
                user_index = self.__cache.index(
                    user_token
                )  # Get the user token position
                tmp_cache = [
                    *self.__cache
                ]  # Transform the cache in a list to replace the value
                tmp_cache[user_index + 1] += (*data,)
                self.__cache = (*tmp_cache,)  # Transform in a tuple
                del tmp_cache  # Delete the cache list
            except ValueError:
                self.__cache += (
                    user_token,
                    data,
                )  # If user is not in cache
            return True
        return False

    def delete(self, value: Any) -> bool:
        """
        Args:
            value (str): user token
        """
        new_cache = [*self.__cache]
        try:
            user_index = new_cache.index(value)
            new_cache.pop(user_index)
            new_cache.pop(user_index + 1)
        except (IndexError, ValueError):
            pass
        self.__cache = (*new_cache,)
        del new_cache
        return True

    def clear_cache(self) -> bool:
        self.__cache = ()
        return True

    def private__transform_user_dict_in_tuple(self, user: dict[str, str]) -> tuple[str]:
        return (
            user["name"],
            user["username"],
        )

    def private__transform_user_tuple_in_dict(
        self, user_tuple: tuple[str]
    ) -> dict[str, str]:
        return {
            "name": user_tuple[0],
            "username": user_tuple[1],
        }
