import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-aristotle-metadata-registry',
    version='0.1',
    packages=['aristotle_mdr'],
    include_package_data=True,
    license='Aristotle-MDR Modified BSD Licence',  # example license
    description='Aristotle-MDR is an open-source metadata registry as laid out by the requirements of the IEC/ISO 11179:2013 specification.',
    long_description=README,
    url='http://github.com/LegoStormtroopr/aristotle-mdr/',
    author='Samuel Spencer',
    author_email='sam@sqbl.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
