#!/usr/bin/env python3
"""
Setup script for Poker Tournament Helper
"""
from setuptools import setup, find_packages

setup(
    name="poker-helper",
    version="0.1.0",
    description="A high-performance web application to help make poker decisions based on probabilities during tournaments",
    author="Poker Helper Team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask>=2.3.3",
        "gunicorn>=21.2.0",
        "treys>=0.1.8",
        "streamlit>=1.32.0",
        "numpy>=1.26.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
