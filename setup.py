"""This module sets up the Mojo CLI app and libraries
"""

from distutils.core import setup

setup(
    name='PyMoJo',
    version='0.9.2',
    author='Ryan Jung',
    author_email='gradysghost@gmail.com',
    packages=['pymojo'],
    url='https://github.com/GradysGhost/pymojo',
    license='LICENSE',
    description='PyJoJo client library',
    long_description=open('README.md').read(),
    install_requires=[
        'requests>=2.4.1',
        'PyYAML>=3.11'
    ],
    entry_points={
        'console_scripts': [
            'mojo = pymojo.cli_bin:main'
        ]
    }
)
