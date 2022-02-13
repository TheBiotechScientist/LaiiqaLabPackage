from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
name = 'DataAnalysis',
version = '1.0.1',
description = 'Package for ozonation, spectro uv and bioreaction data analysis files',
long_description = long_description,
long_description_content_type = 'text/markdown',
license = 'MIT License',
author = 'F. Javier Morales M.',
author_email = 'fmoralesm87@gmail.com',
url = '',
python_requires = '>=3.7',
install_requires = [
    'natsort',
    'numpy',
    'pandas',
    'matplotlib',
    'h5py',
    'sklearn',
    'IPython'
],
packages = find_packages(),
classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.6'
    'Programming Language :: Python :: 3.7',
    'Operating System :: OS Independent',
    'Topic :: Scientific/Engineering'
    ]
)
