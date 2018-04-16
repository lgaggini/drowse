from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name = 'drowse',
    version = '0.2.0',
    author = 'Lorenzo Gaggini',
    author_email = 'lg@lgaggini.net',
    packages = ['drowse'],
    url = 'https://github.com/lgaggini/drowse',
    license = 'LICENSE',
    keywords = ['REST', 'API', 'HTTP'],
    description = 'Human readable slim REST client',
    long_description = long_description,
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP'
    ],
    install_requires = [
        "requests"
    ],
)
