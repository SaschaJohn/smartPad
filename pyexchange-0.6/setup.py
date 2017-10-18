import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
  README = open(os.path.join(here, 'README.md')).read()
  CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except:
  README = ''
  CHANGES = ''

setup(
  name='pyexchange',
  version='0.6',
  url='https://github.com/linkedin/pyexchange',
  license='Apache',
  author='Rachel Sanders',
  author_email='rsanders@linkedin.com',
  maintainer='Rachel Sanders',
  maintainer_email='rsanders@linkedin.com',
  description='A simple library to talk to Microsoft Exchange',
  long_description=README + '\n\n' + CHANGES,
  zip_safe=False,
  test_suite="tests",
  platforms='any',
  include_package_data=True,
  packages=find_packages('.', exclude=['test*']),
  install_requires=['lxml', 'pytz', 'requests', 'requests-ntlm'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)
