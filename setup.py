#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    print 'First, install the pip, please.'
    import sys
    sys.exit(127)

package_folder = 'beget_msgpack'

# Define __version__ without importing beget_amqp.
# This allows building sdist without installing any 3rd party packages.
exec(open(package_folder + '/_version.py').read())

setup(name=package_folder,
      version=__version__,
      description='Client, Server by msgpackrpc and fcgi',
      author='LTD Beget',
      author_email='support@beget.ru',
      url='http://beget.ru',
      license="GPL",
      install_requires=['msgpack-rpc-python', 'py-prefork-server >= 0.4.1'],

      dependency_links=[
          'http://github.com/LTD-Beget/msgpack-rpc-python/tarball/master#egg=msgpack-rpc-python',
          'http://github.com/LTD-Beget/py-prefork-server/tarball/master#egg=py-prefork-server-0.4.1',
      ],

      packages=[package_folder,
                package_folder + '.lib',
                package_folder + '.lib.fastcgi',
                package_folder + '.lib.msgpack',
                package_folder + '.lib.errors',
                package_folder + '.lib.errors.types']
      )
