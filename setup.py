from setuptools import setup, find_packages
import pathlib

# The directory containing this file
ROOOT = pathlib.Path(__file__).parent

# The text of the README file
README = (ROOOT / "README.md").read_text()

setup(
    name='neo4j_connector',
    version="0.1.0",
    author="Dmitry Amanov",
    author_email="",
    description="Neo4j database connector",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/doctor3030/neo4j-connector",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "setuptools>=57",
        "wheel",
        "neo4j==5.6.0"
    ]
)
