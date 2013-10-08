# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013 Infrae. All rights reserved.
# See also LICENSE.txt
from setuptools import setup, find_packages
import os

version = '3.0.3'

tests_require = [
    'Products.Silva [test]',
    'silva.app.news',
    ]

setup(name='silva.app.page',
      version=version,
      description="Silva Extention provides rich content layout object (Silva Page)",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Infrae',
      author_email='info@infrae.com',
      url='http://hg.infrae.com/silva.app.page',
      license='GPL',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['silva', 'silva.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'five.grok',
          'setuptools',
          'silva.core.conf',
          'silva.core.contentlayout',
          'silva.core.interfaces',
          'silva.core.views',
          'silva.core.xml',
          'silva.translations',
          'silva.ui',
          'zeam.form.silva',
          'zope.component',
          'zope.event',
          'zope.i18n',
          'zope.interface',
          'zope.lifecycleevent',
          ],
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      )
