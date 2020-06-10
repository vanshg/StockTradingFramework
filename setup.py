#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="stock-trading-framework",
    version="1.0.0",
    description="Framework for Algorithmically Trading Stocks",
    author="Vansh Gandhi",
    author_email="vansh.gandhi@gmail.com",
    packages=find_packages(),
    install_requires=[
        "schedule",
        "requests",
        "alpaca-trade-api",
    ]
)
