from setuptools import setup, find_packages

setup(
    name="even_odd_analysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "networkx>=2.5",
    ],
)