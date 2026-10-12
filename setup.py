#!/usr/bin/env python3
"""Setup script for Rcolor backward compatibility with legacy tooling."""
from pathlib import Path
from setuptools import find_packages, setup

README_FILE = Path(__file__).parent / "README.md"
long_description = (
    README_FILE.read_text(encoding="utf-8") if README_FILE.is_file() else ""
)

setup(
    name="Rcolor",
    version="3.1.0",
    description=(
        "High-performance Python library for colorful terminal output "
        "with automatic terminal capability detection"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Behnam",
    author_email="Behii@tutanota.com",
    url="https://github.com/ibehii/RandomColorlib",
    license="MIT",
    keywords="terminal color ansi truecolor rainbow cli styling",
    packages=find_packages(),
    package_data={"Rcolor": ["data/*.json", "py.typed"]},
    include_package_data=True,
    install_requires=[
        "colorama>=0.4.6",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Terminals",
        "Typing :: Typed",
    ],
)
