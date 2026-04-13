from setuptools import setup, find_packages

NAME = "managit"
VERSION = "0.1.2"
DESCRIPTION = "Your personal git manager!"
AUTHOR = "Vinny | vgomes-p"
AUTHOR_EMAIL = ""
URL = "https://github.com/vgomes-p/managit"
LICENSE = "MIT"

INSTALL_REQUIRES = []

with open("../README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    license=LICENSE,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "managit=managit.src.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)