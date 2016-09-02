#!/usr/bin/env python
import os
import sys
from getpass import getuser

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    username = getuser()
    settings_file = os.path.join(BASE_DIR, 'ctfspace', 'settings', 'local_{}.py'.format(username))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ctfspace.settings.local_{}".format(username))
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            os.environ['DJANGO_SETTINGS_MODULE'] = 'ctfspace.settings.production'
            import django  # NOQA
            django.setup()
            execute_from_command_line(sys.argv)
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
