from setuptools import setup, find_packages
import os

version = '2.0dev'

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
      author='',
      author_email='',
      url='http://hg.infrae.com/silva.app.page',
      license='GPL',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['silva', 'silva.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'silva.core.conf',
          'silva.core.interfaces',
          'silva.core.contentlayout',
      ]
      )
