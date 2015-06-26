import sys
import os.path
import tempfile

import django
from django.conf import settings
from django.core.management import call_command
from django.utils.crypto import get_random_string
from IPython.core import magic_arguments
from IPython.core.magic import Magics, magics_class, cell_magic, line_cell_magic
from django.utils import six

if six.PY3:
    from importlib import reload


chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

DEFAULT_SETTINGS = {'SECRET_KEY': get_random_string(50, chars),
                    'DATABASES': {
                        'default': {
                            'ENGINE': 'django.db.backends.sqlite3',
                            'NAME': 'db.sqlite' #':memory:'
                        }
                    },
                    'INSTALLED_APPS': ("orm_magic",)
                    }


@magics_class
class DjangoOrmMagics(Magics):

    def _import_all(self, module, verbosity=0):
        imported = []
        for k, v in module.__dict__.items():
            if not k.startswith('__'):
                self.shell.push({k: v})
                imported.append(k)
        if verbosity > 0 and imported:
            print("\nOk. The following django models"
                  "are ready to use: %s" % ", ".join(imported))

    @cell_magic
    def django_orm(self, line, cell):
        j = os.path.join
        if not settings.configured:
            try:
                del self.shell.db['orm_magic_path']
            except KeyError:
                pass
            settings.configure(**DEFAULT_SETTINGS)
            temp_project_path = self.shell.db['orm_magic_path'] = tempfile.mkdtemp()
            sys.path.append(temp_project_path)
            tmp, temp_project = os.path.split(temp_project_path)

            temp_dir = j(temp_project_path, 'orm_magic')
            os.makedirs(temp_dir)
            open(j(temp_project_path, '__init__.py'), 'a').close()
            open(j(temp_dir, '__init__.py'), 'a').close()

        else:
            temp_project_path = self.shell.db['orm_magic_path']
            temp_dir = j(temp_project_path, 'orm_magic')

        module_path = j(temp_dir, 'models.py')
        with open(module_path, 'w') as fh:
            fh.write('\n' + cell)

        django.setup()
        call_command('makemigrations', 'orm_magic', verbosity=0, interactive=False)
        call_command('migrate', 'orm_magic', verbosity=0, interactive=False)

        try:
            reload(orm_magic_models)
        except UnboundLocalError:
            from orm_magic import models as orm_magic_models
        self._import_all(orm_magic_models)
        sys.path.pop()


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(DjangoOrmMagics)
