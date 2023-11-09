from .cache_manager import CacheManager
from .interfaces import CacheInterface

from api.views.views_cache import UsernameCache, UserLettersCache, DetailUserCache

cache_manager_singleton = CacheManager(
    50,
    {
        "username": UsernameCache(),
        "letters_user": UserLettersCache(),
        "user_detail": DetailUserCache(),
    },
)
