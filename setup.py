"""Setup script for the mushroom-segmentation Python package."""
from setuptools import find_packages, setup

setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
