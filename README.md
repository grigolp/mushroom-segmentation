# Mushroom Segmentation

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Mushroom Segmentation** is a computer vision toolkit for detecting, sizing, and analyzing circular mushrooms in agricultural field images. It supports both research and production use cases, including harvesting automation, yield estimation, and quality control.

Built for robustness in real-world environments, it handles uneven lighting, occlusion, and variable mushroom sizes using a combination of classical vision techniques (OpenCV, scikit-image) and domain-specific heuristics.

---

## Key Capabilities

- Accurate segmentation of circular mushrooms from field imagery
- Dual-method radius estimation (with and without normalization)
- Fully configurable pipeline with environment/file-based settings
- Exports detection results to annotated images and structured formats
- Designed for fast batch processing and integration

---

## Documentation

See the complete [Usage Guide](docs/usage.md) for:

- Installation instructions
- CLI and Python API examples
- Configuration and parameter tuning
- Output formats and export options
- Performance and troubleshooting tips

---

## Quick Start

Install from source:
```bash
git clone https://github.com/yourusername/mushroom-segmentation.git
cd mushroom-segmentation
pip install -e .
````

Run on an image:

```bash
mushroom-segment input.jpg -o results.csv --save-visualization annotated.png
```

Or use as a Python module:

```python
from mushroom_segmentation import MushroomSegmenter, ImageIO, Settings

image = ImageIO().load_image("image.jpg")
segmenter = MushroomSegmenter(Settings())
results = segmenter.segment(image)
```

---

## Project Structure s

* `src/`: Core segmentation library
* `examples/`: Example images, usage scripts
* `docs/`: Extended documentation

---


## License

This project is licensed under the [MIT License](LICENSE).
