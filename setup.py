from setuptools import setup

setup(
    name="configloader",
    version="0.1.1",
    description="Config Parser and Loader",
    url="https://git.liateam.net/python/packages/configloader.git",
    author="Shahab Ghosni",
    author_email="s.ghosni@liateam.ir",
    license="BSD 2-clause",
    packages=["configloader"],
    install_requires=[
        "annotated-types >= 0.5.0",
        "configparser >= 6.0.0",
        "pydantic >= 1.10.0",
        "pydantic_core >= 2.4.0",
        "typing_extensions >= 4.7.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
