"""Mushroom Segmentation Package.

A robust image processing library for detecting and analyzing circular objects in images,
with special optimization for mushroom detection in agricultural and research applications.
"""

from .core.segmentation import MushroomSegmenter
from .core.visualization import Visualizer
from .utils.io_handler import ImageIO, ResultsExporter

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "MushroomSegmenter",
    "Visualizer",
    "ImageIO",
    "ResultsExporter",
]
