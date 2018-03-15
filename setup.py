#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'django-filter>=1.1.0',
    'django-mptt==0.9.0',
    'Django',
    'djangorestframework>3',
    'jsonschema==2.6.0',
    'django-nested-admin==3.0.21',
    'django-jsonschema-form==1.0.2',
    'django-bower==5.2.0'
]
setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

packages = find_packages(include=['cms', 'cms.migrations', 'cms.management', 'cms.static', 'cms.management.commands'])
print("Packages Included in this Setup.py: %s" % str(packages))

setup(
    author="David G. Daniel",
    author_email='davydany@aeroxis.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.8',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    description="Gophr CMS is the CMS for Professionals with Deadlines.",
    entry_points={
        'console_scripts': [
            'gophr=gophr.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='gophr',
    name='gophr',
    packages=packages,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/davydany/gophr',
    version='0.1.8',
    zip_safe=False,
)
