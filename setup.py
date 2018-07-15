#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(name='pysong',
                 version='0.1.0',
                 description='PySong searches for a song by a line of lyrics',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='https://github.com/paper-lark/pysong',
                 author='Max Zhuravsky',
                 author_email='paperlark@yandex.com',
                 license='MIT',
                 packages=['pysong'],
                 install_requires=[
                     'beautifulsou4', 'lxml', 'requests'
                 ])
