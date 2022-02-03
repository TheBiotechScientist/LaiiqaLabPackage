from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
name = 'DataAnalysis',
version = '1.0.0',
description = 'Package for ozonation and spectro uv data analysis files',
long_description = long_description,
long_description_content_type = 'text/markdown',
license = 'MIT License',
author = 'F. Javier Morales',
author_email = 'fmoralesm87@gmail.com',
url = '',
python_requires = '>=3.7',
install_requires = [
    'natsort',
    'numpy',
    'pandas',
    'matplotlib',
    'h5py',
    'sklearn'
],
packages = find_packages(),
classifiers = [
    'Development Status :: 1 - Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Operating System :: OS Independent',
    'Topic :: Data Science'
    ]
)
