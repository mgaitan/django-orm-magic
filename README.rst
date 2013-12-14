=================
Django ORM Magic
=================

.. image:: https://pypip.in/v/django-orm-magic/badge.png
   :target: https://pypi.python.org/pypi/django-orm-magic
   :alt: Latest PyPI version

.. image:: https://pypip.in/d/django-orm-magic/badge.png
   :target: https://pypi.python.org/pypi/django-orm-magic
   :alt: Number of PyPI downloads


:author: Martín Gaitán <gaitan@gmail.com>
:homepage: https://github.com/mgaitan/django-orm-magic
:documentation: see `this notebook`__

__ documentation_
.. _documentation:  http://nbviewer.ipython.org/urls/raw.github.com/mgaitan/django-orm-magic/master/documentation.ipynb


Define your django models in an IPython cell and use them on the fly.
Let the magic do the boring part.

Django ORM isn't not conceived to be used standalone. Even for a trivial case, you need to configure a database, create an app, etc. This magic handle that automatically, and then import every model to your interactive session.


Install
=======

You can install or upgrade via pip

    pip install -U django-orm-magic

or directly from the repository using the `%install_ext` magic command::

    In[1]: %install_ext https://raw.github.com/mgaitan/django-orm-magic/master/django_orm_magic.py


Basic usage
===========

Once it's installed, you can load it with ``%load_ext django_orm_magic``. Then define your models in a cell started with the cell magic ``%%django_orm``.
For example::

    In[2]: %load_ext django_orm_magic


    In[3]: %%django_orm

           from django.db import models

           class Poll(models.Model):
               question = models.CharField(max_length=200)
               pub_date = models.DateTimeField('date published')

           class Choice(models.Model):
               poll = models.ForeignKey(Poll)
               choice_text = models.CharField(max_length=200)
               votes = models.IntegerField(default=0)


And it's done. Every model is synced in a sqlite database named ``db.sqlite`` in your current path and imported automatically::


    In[4]: Poll.objects.all()
    Out[4]: []

    In[5]: from django.utils import timezone
           p = Poll(question="What's new?", pub_date=timezone.now())
           p.save()


See the documentation_ for further details.

See here_ for another example

.. _here: http://nbviewer.ipython.org/gist/mgaitan/7224431#modelando-resultados.gob.ar-en-una-base-de-datos