=========
Gophr CMS
=========


.. image:: https://img.shields.io/pypi/v/gophr.svg
        :target: https://pypi.python.org/pypi/gophr

.. image:: https://img.shields.io/travis/davydany/gophr.svg
        :target: https://travis-ci.org/davydany/gophr

.. image:: https://readthedocs.org/projects/gophr/badge/?version=latest
        :target: https://gophr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Gophr CMS is the CMS for Professionals with Deadlines.


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

1. Install from PyPI:

.. highlight:: bash
    :linenos:

    pip install gophr

2. Add Gophr and it's dependencies to your INSTALLED_APPS

.. highlight:: python
    :linenos:

    INSTALLED_APPS = [
        ...
        'mptt',
        'nested_admin',
        'jsonschemaform',
        'cms',
    ]

3. Setup Django by Migrating and Collecting Static

.. highlight:: bash
    :linenos:

    python manage.py collectstatic --noinput
    python manage.py migrate

4. Start your Gophr CMS

.. highlight:: bash
    :linenos:

    python manage.py runserver
