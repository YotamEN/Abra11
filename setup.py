from setuptools import setup, find_packages

setup(
    name='Abra',
    author='Yotam Even-Nir',
    description='Advanced System Design course final project',
    packages=find_packages(),
    install_requires=['click', 'flask'],
    tests_require=['pytest', 'pytest-cov']
)
