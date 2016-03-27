from setuptools import setup

setup(name = 'echidna',
      version = '0.0.1',
      packages = ['echidna'],
      entry_points = {
          'console_scripts': [
              'echidna = echidna.__main__:main'
          ]
      },
      install_requires = [
          'python-daemon',
          'lockfile'
      ]
     )
