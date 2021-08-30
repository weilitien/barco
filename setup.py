from setuptools import setup, find_packages

PACKAGE_VERSION = '1.0'


# dependencies
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='barcotest',
      version=PACKAGE_VERSION,
      description='WebUI and API test for Barco',
      keywords='Barco',
      author='Willie Tien',
      author_email='godlisi@hotmail.com',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requirements
      )
