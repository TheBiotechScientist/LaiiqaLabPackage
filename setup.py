from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(
name = 'laiiqa-lab-utilities',
version = '0.1.1',
description = 'Package for ozonation, spectro uv and bioreaction data analysis files for the LAIIQA laboratory (ESIQIE - IPN).',
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
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Operating System :: OS Independent',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS',
    'Operating System :: POSIX :: Linux',
    'Topic :: Scientific/Engineering',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Intended Audience :: Education'
    ]
)
