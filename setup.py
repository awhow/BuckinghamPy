
from setuptools import setup, find_packages

exec(open('buckinghampy/version.py').read())

setup(name='buckinghampy',
      version=__version__,
      packages=find_packages(),
      install_requires=['numpy'],
      url='https://github.com/awhow/BuckinghamPy',
      author='Aaron Howell',
      author_email='aaron.winter.howell@gmail.com')
