#!/usr/bin/env python
import os
import sys

from django.core.management import execute_from_command_line


def jupyter():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    try:
        import django_extensions
    except ImportError:
        raise ImportError("Необходимо установить django-extensions чтобы запустить юпитер (а также сам юпитер)")
    argv = sys.argv + ['shell_plus', '--notebook']
    execute_from_command_line(sys.argv + ['makemigrations', 'tests'])
    execute_from_command_line(sys.argv + ['migrate'])
    execute_from_command_line(argv)


if __name__ == "__main__":
    jupyter()
