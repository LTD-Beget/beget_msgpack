#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    print 'First, install the pip, please.'
    import sys
    sys.exit(127)

package_folder = 'beget_msgpack'

setup(name=package_folder,
      version='0.1.0',
      description='Client, Server by msgpackrpc',
      author='LTD Beget',
      author_email='support@beget.ru',
      url='http://beget.ru',
      license="GPL",
      install_requires=['msgpack-rpc-python'],
      packages=[package_folder])
