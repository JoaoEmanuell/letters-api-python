#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

from main.setup import create_database, copy_settings


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if not os.path.exists(
        os.path.join(BASE_DIR, "database", "migrates.txt")
    ):  # Make migrations on the first execution
        create_database()
        copy_settings()
        execute_from_command_line(["manage.py", "makemigrations", "api"])
        execute_from_command_line(["manage.py", "migrate"])
        with open(os.path.join(BASE_DIR, "database", "migrates.txt"), "w") as file:
            file.write("true")
    else:
        # Copy settings on execute the server
        copy_settings()
    execute_from_command_line(sys.argv)  # Run the server


if __name__ == "__main__":
    main()
