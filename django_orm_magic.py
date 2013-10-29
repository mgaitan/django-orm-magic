import imp
import sys
import os.path
import tempfile

from django.core.management import call_command
from django.utils.crypto import get_random_string
from django.conf import settings
from IPython.core.magic import Magics, magics_class,  cell_magic


chars = 'abcdefghijklmnopqrstuvwxyz0123456789'


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
        temp_project = tempfile.mkdtemp()
        temp_dir = os.path.join(temp_project, 'orm_magic')
        os.makedirs(temp_dir)

        open(os.path.join(temp_dir, '__init__.py'), 'a').close()

        module_path = os.path.join(temp_dir, 'models.py')
        with open(module_path, 'w') as fh:
            fh.write(cell)
        print temp

        sys.path.insert(1, temp_dir)

        settings.configure(SECRET_KEY=secret_key, INSTALLED_APPS=('orm_magic',),
                           DATABASES = {'default':
                                        {'ENGINE': 'django.db.backends.sqlite3',
                                                   'NAME': ':memory:'}})
        call_command('syncdb', verbosity=0,) #)interactive=False)
        module = imp.load_dynamic('models', module_path)
        self._import_all(module)
        sys.path.pop(1)


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(DjangoOrmMagics)
