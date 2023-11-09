from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def generate_token_hex() -> str:
    from secrets import token_hex

    return token_hex(32)


def generate_fernet_key() -> bytes:
    from cryptography.fernet import Fernet

    return Fernet.generate_key()


def create_letters_dir() -> None:
    from os import mkdir
    from os.path import exists

    global BASE_DIR

    path_to_letters = f"{BASE_DIR}/database/letters/"
    if not exists(path_to_letters):
        mkdir(path_to_letters)


def copy_settings() -> None:
    from os.path import exists

    global BASE_DIR

    if not exists(f"{BASE_DIR}/database/backup/settings.py"):
        with open("settings_example.py", "r") as settings_example:
            settings_example = settings_example.read()
            with open("settings.py", "w") as settings:
                settings_with_secret_key = _write_django_secret_key(settings_example)
                settings.write(settings_with_secret_key)
                # Cryptograph to models
                cryptograph_key = []
                for _ in range(9):  # Number of keys to generate, used to models
                    cryptograph_key.append(generate_token_hex())

                cryptograph_str = f"\n\n# Encrypted fields\n\nFIELD_ENCRYPTION_KEYS = {cryptograph_key}\n"

                settings.write(cryptograph_str)

                # Cryptograph to letters
                cryptograph_str = (
                    f"\n\n# Fernet key\n\nFERNET_KEY = {generate_fernet_key()}\n"
                )

                settings.write(cryptograph_str)

        backup_settings()
    else:
        restore_settings()


def backup_settings() -> None:
    from os.path import exists
    from os import mkdir

    global BASE_DIR

    backup_dir = f"{BASE_DIR}/database/backup"

    if not exists(backup_dir):
        mkdir(backup_dir)

    with open("settings.py", "r") as settings:
        with open(f"{backup_dir}/settings.py", "w") as settings_backup:
            settings_backup.write(settings.read())


def restore_settings() -> None:
    global BASE_DIR

    backup_dir = f"{BASE_DIR}/database/backup"
    with open(f"{backup_dir}/settings.py", "r") as settings_backup:
        with open("settings.py", "w") as settings:
            settings.write(settings_backup.read())


def _write_django_secret_key(settings: str) -> str:
    from django.core.management.utils import get_random_secret_key

    settings_with_secret = settings
    settings_with_secret = settings_with_secret.replace(
        'SECRET_KEY = "our_secret_here"',
        f'SECRET_KEY = "{get_random_secret_key()}"',
    )
    return settings_with_secret


def create_database() -> None:
    from os import mkdir
    from os.path import exists

    global BASE_DIR

    path_to_database = f"{BASE_DIR}/database"
    # Create database dir
    if not exists(path_to_database):
        mkdir(path_to_database)

    # Create sqlite3 db
    if not exists(f"{path_to_database}/db.sqlite3"):
        with open(f"{path_to_database}/db.sqlite3", "w") as file:
            file.write("")

    # Create letters
    path_to_letters = f"{path_to_database}letters/"
    if not exists(path_to_letters):
        mkdir(path_to_letters)


if __name__ == "__main__":
    # Create database
    create_database()

    # Copy settings
    copy_settings()
