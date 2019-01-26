#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="umling",
    version="0.0.1",
    author="Ivan Semkin",
    author_email="ivan@semkin.ru",
    description="Interactively generate Use-Case UML diagrams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanyasem/umling",
    license='GPLv3+',
    packages=setuptools.find_packages(),
    install_requires=[
        'pymorphy2==0.8',
        'pydot==1.4.1',
        'python-telegram-bot==11.1.0',
        'cefpython3==66.0',
        'peewee==3.8.2'
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: Russian",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
