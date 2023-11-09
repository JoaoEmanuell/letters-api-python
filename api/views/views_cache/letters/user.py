from typing import Any
from datetime import datetime

from main.cache_manager import CacheInterface


class UserLettersCache(CacheInterface):
    def __init__(self) -> None:
        self.__cache = ()
        """
        Cache model:
        (
            "user_token", (("date", "sender", "text", "letter_token"), ), 
        )
        """
        self.__cache_expire = ()  # (User token, date)
        self.__CACHE_EXPIRE_MINUTES = 5  # Minutes to expire the cache

    def get(self, value: Any) -> Any | None:
        """

        Args:
            value (Any): user_token

        Returns:
            List | None: List with user letters or None
        """
        if value in self.__cache and not self.private__get_cache_expire(value):
            letters = self.__cache[self.__cache.index(value) + 1]
            data = self.private__mount_letters_list(letters)
            return data

        return None

    def set(self, value: Any) -> bool:
        """
        Args:
            value (dict): {"user_token": str, "letters": [...]}

        Returns:
            bool: _description_
        """
        user_token = value["user_token"]
        letters = value["letters"]
        if not self.get(user_token):  # If has user letters in the cache
            letters_tuple = self.private__transform_letters_dict_in_tuple(letters)
            try:
                user_index = self.__cache.index(
                    user_token
                )  # Get the user token position
                tmp_cache = [
                    *self.__cache
                ]  # Transform the cache in a list to replace the value
                tmp_cache[user_index + 1] += (*letters_tuple,)
                self.__cache = (*tmp_cache,)  # Transform in a tuple
                del tmp_cache  # Delete the cache list
            except ValueError:
                self.__cache += (
                    user_token,
                    letters_tuple,
                )  # If user is not in cache
            self.private__set_user_cache_expire(user_token)  # Set the expire time
            return True
        return False

    def delete(self, value: Any) -> bool:
        new_cache = [*self.__cache]
        try:
            user_index = new_cache.index(value)
            new_cache.pop(user_index)
            new_cache.pop(user_index + 1)
        except (IndexError, ValueError):
            pass
        self.__cache = (*new_cache,)
        del new_cache
        self.private__delete_user_cache_expire(value)
        return True

    def clear_cache(self) -> bool:
        self.__cache = ()
        self.__cache_expire = ()
        return True

    def private__mount_letters_list(
        self, letters_tuple: tuple[tuple[str]]
    ) -> list[dict[str, str]]:
        """Transform the saved letters tuple on list to return

        Args:
            letters_tuple (tuple[tuple[str]]): Tuple with saved letters

        Returns:
            list[dict[str, str]]: List with letters
        """
        letters: list[dict[str, str]] = []
        for letter in letters_tuple:
            data = {
                "date": letter[0].encode(),
                "sender": letter[1].encode(),
                "text": letter[2].encode(),
                "letter_token": letter[3].encode(),
            }
            letters.append(data)

        return letters

    def private__transform_letters_dict_in_tuple(
        self, letters: list[dict[str, str]]
    ) -> tuple[tuple[str]]:
        """Transform the letters dict on tuple to save

        Args:
            letters (list[dict[str, str]]): List with letters object

        Returns:
            tuple[tuple[str]]: Tuple of tuple with letters
        """
        letters_tuple = ()
        for letter in letters:
            letters_tuple += (
                (
                    letter["date"],
                    letter["sender"],
                    letter["text"],
                    letter["letter_token"],
                ),
            )

        return letters_tuple

    def private__get_cache_expire(self, user_token: str) -> bool:
        """Config cache expire time

        Args:
            user_token (str): user token

        Returns:
            bool: True if cache expire or False if not
        """
        try:
            user_datetime: datetime = self.__cache_expire[
                self.__cache_expire.index(user_token) + 1
            ]
            now_date = datetime.now()
            hour, minute = (now_date.hour, now_date.minute)
            if (
                user_datetime.hour < hour
                or user_datetime.minute + self.__CACHE_EXPIRE_MINUTES < minute
            ):
                return True
            return False
        except ValueError:
            return True

    def private__set_user_cache_expire(self, user_token: str) -> None:
        """Set the user cache expire time

        Args:
            user_token (str): user token
        """
        new_cache = [*self.__cache]
        user_index = new_cache.index(user_token)
        new_cache[user_index + 1] = datetime.now()
        self.__cache_expire = (*new_cache,)
        del new_cache

    def private__delete_user_cache_expire(self, user_token: str) -> None:
        """Delete the user cache expire time

        Args:
            user_token (str): user token
        """
        new_cache = [*self.__cache]
        try:
            user_index = new_cache.index(user_token)
            new_cache.pop(user_index)
            new_cache.pop(user_index + 1)
        except (ValueError, IndexError):
            pass
        self.__cache_expire = (*new_cache,)
