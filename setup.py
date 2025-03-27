"""Setup script for the AUTOCLICK package."""
import os
from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements from requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

# Get version from version.py
version = {}
with open(os.path.join("src", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version)

setup(
    name="autoclick",
    version=version["__version__"],
    description="A streamlined, maintainable, and easily extensible web automation application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Phazzie",
    author_email="phazziezee@gmail.com",
    url="https://github.com/Phazzie/autoclick",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "autoclick": ["py.typed"],
    },
    install_requires=requirements,
    extras_require={
        "dev": [
            "black",
            "isort",
            "pylint",
            "mypy",
            "pytest",
            "pytest-cov",
            "coverage",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "autoclick=src.cli.main:main",
        ],
    },
)
