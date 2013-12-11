import importlib
import sys
import os.path
import tempfile

from django.core.management import call_command
from django.utils.crypto import get_random_string
from IPython.core.magic import Magics, magics_class, cell_magic


chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

settings_tpl = """
SECRET_KEY = '%s'
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.sqlite' #':memory:'
    }
  }
INSTALLED_APPS = ("orm_magic",)
"""


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
        secret_key = get_random_string(50, chars)
        j = os.path.join

        temp_project_path = tempfile.mkdtemp()
        tmp, temp_project = os.path.split(temp_project_path)

        temp_dir = j(temp_project_path, 'orm_magic')
        os.makedirs(temp_dir)
        print temp_dir
        open(j(temp_project_path, '__init__.py'), 'a').close()
        open(j(temp_dir, '__init__.py'), 'a').close()

        module_path = j(temp_dir, 'models.py')
        with open(module_path, 'w') as fh:
            fh.write(cell)
        with open(j(temp_dir, 'settings.py'), 'w') as fh:
            fh.write(settings_tpl % secret_key)

        sys.path.append(temp_project_path)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'orm_magic.settings'
        call_command('syncdb', verbosity=0, interactive=False)

        module = importlib.import_module('orm_magic.models', temp_project)
        self._import_all(module)
        sys.path.pop()


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(DjangoOrmMagics)
