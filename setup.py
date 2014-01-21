# -*- coding: utf-8 -*-
from setuptools import setup

long_description = (open('README.rst').read() + '\n\n' +
                    open('CHANGES.rst').read())

setup(
    name='django-orm-magic',
    version='0.3.1',
    description="An extension for IPython that help to define django's models in "
                "your interactive session.",
    long_description=long_description,
    author='Martin Gaitan',
    author_email='gaitan@gmail.com',
    url='https://github.com/mgaitan/django-orm-magic',
    license='BSD',
    keywords="ipython notebook django orm standalone",
    py_modules=['django_orm_magic'],
    install_requires=['ipython', 'django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: IPython',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
)
