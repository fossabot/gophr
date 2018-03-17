=========
Gophr CMS
=========


.. image:: https://img.shields.io/pypi/v/gophr.svg
        :target: https://pypi.python.org/pypi/gophr

.. image:: https://img.shields.io/travis/aeroxis/gophr.svg
        :target: https://travis-ci.org/aeroxis/gophr

.. image:: https://readthedocs.org/projects/gophr-cms/badge/?version=latest
        :target: https://gophr-cms.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Gophr CMS is the CMS for Professionals with Deadlines. 

Gophr CMS is a headless CMS built on Django. It is designed with backend developers, frontend developers, content editors
and project managers in mind. 


* Free software: MIT license
* Documentation: https://github.com/aeroxis/gophr.


Features
--------

* CMS for Page Data Management
    * Create multiple sections for any given page
    * Create multiple components for each section
        * Components follow a strict ComponentType to ensure all it's required values are set


Getting Started
---------------

* Install from PyPI:

.. code:: python

  pip install gophr

* Add Gophr and it's dependencies to your INSTALLED_APPS

.. code:: python

  INSTALLED_APPS = [
      ...
      'mptt',
      'nested_admin',
      'jsonschemaform',
      'cms',
  ]

* Setup Django by Migrating and Collecting Static

.. code:: python

  python manage.py collectstatic --noinput
  python manage.py migrate

* Start your Gophr CMS


.. code:: python

  python manage.py runserver
