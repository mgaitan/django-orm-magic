import importlib
import sys
import os.path
import tempfile

from django.core.management import call_command
from django.utils.crypto import get_random_string
from IPython.core import magic_arguments
from IPython.core.magic import Magics, magics_class, cell_magic, line_cell_magic


chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

secret_key = """
SECRET_KEY = '%s'
""" % get_random_string(50, chars)

settings_default = """
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

    def get_settings(self, add_secret_key=False):
        try:
            settings = self.shell.db['django_orm']
        except KeyError:
            settings = settings_default
        if add_secret_key:
            settings = secret_key + settings
        return settings

    def _import_all(self, module, verbosity=0):
        imported = []
        for k, v in module.__dict__.items():
            if not k.startswith('__'):
                self.shell.push({k: v})
                imported.append(k)
        if verbosity > 0 and imported:
            print("\nOk. The following django models"
                  "are ready to use: %s" % ", ".join(imported))

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        '--default', action="store_true", help="Delete custom settings "
        "and back to the default"
    )
    @line_cell_magic
    def django_settings(self, line, cell=""):
        """
        Show and setup the django settings to use with %%django_orm

            %django_settings

                Load the current custom configuration in a new cell

            %django_settings --default

                Delete the current configuration and back to the default

            %%django_settings

            DATABASES = {
              'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite' #':memory:'
                }
              }
            INSTALLED_APPS = ("orm_magic",)
        """
        args = magic_arguments.parse_argstring(self.django_settings, line)
        if args.default:
            try:
                del self.shell.db['django_orm']
                print("Deleted custom settings. Back to default for %%django_orm")
            except KeyError:
                print("No custom settings found for %%django_orm")
        elif not line and not cell:
            self.shell.set_next_input("%%django_settings\n" + self.get_settings())
        else:
            self.shell.db['django_orm'] = cell
            print("Settings for %%django_orm configured succesfully")

    @cell_magic
    def django_orm(self, line, cell):
        j = os.path.join

        temp_project_path = tempfile.mkdtemp()
        tmp, temp_project = os.path.split(temp_project_path)

        temp_dir = j(temp_project_path, 'orm_magic')
        os.makedirs(temp_dir)
        open(j(temp_project_path, '__init__.py'), 'a').close()
        open(j(temp_dir, '__init__.py'), 'a').close()

        module_path = j(temp_dir, 'models.py')
        with open(module_path, 'w') as fh:
            fh.write(cell)
        with open(j(temp_dir, 'settings.py'), 'w') as fh:
            fh.write(self.get_settings(True))

        sys.path.append(temp_project_path)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'orm_magic.settings'
        call_command('syncdb', verbosity=0, interactive=False)

        module = importlib.import_module('orm_magic.models', temp_project)
        self._import_all(module)
        sys.path.pop()


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(DjangoOrmMagics)
