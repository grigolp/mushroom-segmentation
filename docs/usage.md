# Complete Usage Guide

This guide covers all ways to use the mushroom-segmentation library, from simple command-line usage to advanced Python integration.

## Table of Contents

1. [Installation](#installation)
2. [Command Line Usage](#command-line-usage)
3. [Python Library Usage](#python-library-usage)
4. [Configuration](#configuration)
5. [Input/Output Formats](#inputoutput-formats)
6. [Performance Tips](#performance-tips)
7. [Troubleshooting](#troubleshooting)

## Installation

### From PyPI (when published)
```bash
pip install mushroom-segmentation
```

### From GitHub
```bash
git clone https://github.com/yourusername/mushroom-segmentation.git
cd mushroom-segmentation
pip install .
```

### Development Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/mushroom-segmentation.git
cd mushroom-segmentation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```


## Command Line Usage

### Basic Usage

The simplest way to use the tool:

```bash
mushroom-segment image.jpg
```

This will:
- Process `image.jpg`
- Save results to `results.csv`
- Display visualization on screen

### All Command Line Options

```bash
mushroom-segment --help
```

Available options:

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--output-csv` | `-o` | results.csv | Output CSV file path |
| `--visualize/--no-visualize` | | --visualize | Display results on screen |
| `--save-visualization` | `-s` | None | Save annotated image |
| `--config` | `-c` | None | Configuration file path |
| `--back-threshold` | | 100 | Background threshold (0-255) |
| `--threshold` | | 150 | Segmentation threshold (0-255) |
| `--min-diameter` | | 30 | Minimum diameter in pixels |
| `--peaks-threshold` | | 0.1 | Peak detection threshold (0-1) |

### Command Line Examples

#### Process with custom parameters:
```bash
mushroom-segment field.jpg \
  --back-threshold 80 \
  --threshold 120 \
  --min-diameter 40 \
  --output-csv field_results.csv
```

#### Save visualization without display:
```bash
mushroom-segment image.jpg \
  --no-visualize \
  --save-visualization annotated.png
```

#### Use configuration file:
```bash
mushroom-segment image.jpg --config my_settings.env
```

#### Batch processing with shell script:
```bash
#!/bin/bash
for img in images/*.jpg; do
    output="results/$(basename $img .jpg)_results.csv"
    mushroom-segment "$img" -o "$output" --no-visualize
done
```

## Python Library Usage

### Basic Example

```python
from mushroom_segmentation import MushroomSegmenter, ImageIO
from mushroom_segmentation.config import Settings

# Load image
image_io = ImageIO()
image = image_io.load_image("mushroom.jpg")

# Create segmenter with default settings
segmenter = MushroomSegmenter(Settings())

# Detect mushrooms
circles = segmenter.segment(image)

# Process results
print(f"Found {len(circles)} mushrooms")
for x, y, r1, r2 in circles:
    print(f"  Position: ({x}, {y}), Radius: {r1}")
```

### Custom Settings

```python
from mushroom_segmentation.config import Settings

# Method 1: Direct parameters
settings = Settings(
    back_threshold=80,
    threshold=120,
    min_diameter=40,
    peaks_rel_threshold=0.15,
    gaussian_kernel_size=7,
    clahe_clip_limit=3.0
)

# Method 2: From .env file
settings = Settings(_env_file="custom.env")

# Method 3: From dictionary
config_dict = {
    "back_threshold": 80,
    "threshold": 120,
    "min_diameter": 40
}
settings = Settings(**config_dict)

# Use the settings
segmenter = MushroomSegmenter(settings)
```

### Export Results

```python
from mushroom_segmentation import ResultsExporter

exporter = ResultsExporter()

# Export to CSV
exporter.to_csv(circles, "results.csv")

# Export to CSV without header
exporter.to_csv(circles, "results_no_header.csv", header=False)

# Export to JSON with metadata
metadata = {
    "image_file": "mushroom.jpg",
    "processing_date": "2024-01-15",
    "settings": settings.model_dump(),
    "processing_time": 0.523
}
exporter.to_json(circles, "results.json", metadata)
```

### Visualization Options

```python
from mushroom_segmentation import Visualizer

visualizer = Visualizer()

# Basic visualization
annotated = visualizer.draw_circles(image, circles)

# Custom colors (BGR format)
visualizer.settings.center_color = (0, 255, 255)  # Yellow centers
visualizer.settings.radius1_color = (255, 0, 0)   # Blue circles
visualizer.settings.radius2_color = (0, 0, 255)   # Red circles

# Create overlay
overlay = visualizer.create_overlay(image, circles, alpha=0.4)

# Side-by-side comparison
comparison = visualizer.create_comparison(
    original=image,
    processed=annotated,
    orientation="horizontal"  # or "vertical"
)

# Display in window
visualizer.display(annotated, window_name="My Results")

# Save visualizations
image_io = ImageIO()
image_io.save_image(annotated, "annotated.jpg")
image_io.save_image(overlay, "overlay.png")
image_io.save_image(comparison, "comparison.jpg")
```

### Batch Processing

```python
from pathlib import Path
import time

def process_directory(input_dir, output_dir):
    """Process all images in a directory."""

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Initialize components
    settings = Settings()
    segmenter = MushroomSegmenter(settings)
    image_io = ImageIO()
    exporter = ResultsExporter()
    visualizer = Visualizer()

    # Track statistics
    total_mushrooms = 0
    processing_times = []

    # Process each image
    for image_file in input_path.glob("*.jpg"):
        print(f"Processing {image_file.name}...")

        start_time = time.time()

        # Load and process
        image = image_io.load_image(image_file)
        circles = segmenter.segment(image)

        processing_time = time.time() - start_time
        processing_times.append(processing_time)

        # Save results
        csv_file = output_path / f"{image_file.stem}_results.csv"
        exporter.to_csv(circles, csv_file)

        # Save visualization
        annotated = visualizer.draw_circles(image, circles)
        vis_file = output_path / f"{image_file.stem}_annotated.jpg"
        image_io.save_image(annotated, vis_file)

        # Update statistics
        total_mushrooms += len(circles)
        print(f"  Found {len(circles)} mushrooms in {processing_time:.2f}s")

    # Summary
    print(f"\nProcessing complete!")
    print(f"Total images: {len(processing_times)}")
    print(f"Total mushrooms: {total_mushrooms}")
    print(f"Average time: {sum(processing_times)/len(processing_times):.2f}s")

# Use it
process_directory("input_images", "output_results")
```

## Configuration

### Configuration Methods

1. **Environment Variables**
```bash
export BACK_THRESHOLD=100
export THRESHOLD=150
export MIN_DIAMETER=30
```

2. **.env File**
```env
# Segmentation parameters
BACK_THRESHOLD=100
THRESHOLD=150
MIN_DIAMETER=30
PEAKS_REL_THRESHOLD=0.1

# Image processing
GAUSSIAN_KERNEL_SIZE=5
CLAHE_CLIP_LIMIT=2.0
CLAHE_TILE_SIZE=8

# Visualization
CENTER_COLOR=[255,0,0]
RADIUS1_COLOR=[0,255,0]
RADIUS2_COLOR=[0,0,255]
LINE_THICKNESS=2
```

3. **JSON Configuration**
```json
{
  "back_threshold": 100,
  "threshold": 150,
  "min_diameter": 30,
  "peaks_rel_threshold": 0.1,
  "gaussian_kernel_size": 5,
  "clahe_clip_limit": 2.0
}
```

Load JSON config:
```python
import json
from mushroom_segmentation.config import Settings

with open('config.json') as f:
    config = json.load(f)

settings = Settings(**config)
```

### Parameter Guidelines

| Parameter | Low Values | High Values | Use Case |
|-----------|------------|-------------|----------|
| `back_threshold` | More background included | Less background | Dark backgrounds → lower |
| `threshold` | Larger detected objects | Smaller objects | Bright mushrooms → higher |
| `min_diameter` | Detects smaller objects | Filters small objects | Noisy images → higher |
| `peaks_rel_threshold` | More objects detected | Fewer objects | Dense clusters → higher |

## Input/Output Formats

### Supported Input Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tif, .tiff)

### CSV Output Format
```csv
X,Y,Radius_1,Radius_2
234,567,45,47
123,456,38,40
345,234,52,54
```

### JSON Output Format
```json
{
  "circles": [
    {
      "x": 234,
      "y": 567,
      "radius_1": 45,
      "radius_2": 47
    }
  ],
  "count": 3,
  "metadata": {
    "image": "mushrooms.jpg",
    "settings": {...},
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

## Performance Tips

### For Faster Processing

1. **Resize Large Images**
```python
import cv2

# Resize if image is too large
image = image_io.load_image("huge_image.jpg")
if image.shape[0] > 2000 or image.shape[1] > 2000:
    scale = 2000 / max(image.shape[:2])
    new_size = (int(image.shape[1] * scale), int(image.shape[0] * scale))
    image = cv2.resize(image, new_size)
```

2. **Process in Parallel**
```python
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

def process_single_image(image_path):
    image = ImageIO.load_image(image_path)
    circles = MushroomSegmenter(Settings()).segment(image)
    return image_path.name, len(circles)

# Process multiple images in parallel
image_files = list(Path("images").glob("*.jpg"))

with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_single_image, image_files)

for filename, count in results:
    print(f"{filename}: {count} mushrooms")
```

3. **Optimize Parameters**
```python
# For simple, high-contrast images
fast_settings = Settings(
    gaussian_kernel_size=3,  # Less blur
    clahe_clip_limit=1.5,    # Less enhancement
    morphology_kernel_size=3  # Faster morphology
)

# For complex, low-contrast images
quality_settings = Settings(
    gaussian_kernel_size=7,   # More blur
    clahe_clip_limit=3.0,     # More enhancement
    peaks_rel_threshold=0.15  # More selective
)
```

## Troubleshooting

### Common Issues and Solutions

#### No mushrooms detected
```python
# Solution 1: Lower thresholds
settings = Settings(
    back_threshold=50,      # Was 100
    threshold=100,          # Was 150
    peaks_rel_threshold=0.05  # Was 0.1
)

# Solution 2: Check image loading
image = image_io.load_image("image.jpg")
print(f"Image shape: {image.shape}")
print(f"Image dtype: {image.dtype}")
print(f"Value range: {image.min()} - {image.max()}")
```

#### Too many false detections
```python
# Solution: Increase filtering
settings = Settings(
    min_diameter=50,         # Was 30
    peaks_rel_threshold=0.2  # Was 0.1
)
```

#### Incorrect radius measurements
```python
# Check both radius values
for x, y, r1, r2 in circles:
    # r1: Standard processing
    # r2: With histogram equalization
    # Use r2 for low-contrast images
    radius = r2 if low_contrast else r1
```

#### Memory issues with large images
```python
# Process in chunks
def process_large_image(image_path, chunk_size=1000, overlap=100):
    full_image = image_io.load_image(image_path)
    height, width = full_image.shape[:2]

    all_circles = []

    for y in range(0, height, chunk_size - overlap):
        for x in range(0, width, chunk_size - overlap):
            # Extract chunk
            chunk = full_image[
                y:min(y + chunk_size, height),
                x:min(x + chunk_size, width)
            ]

            # Process chunk
            circles = segmenter.segment(chunk)

            # Adjust coordinates
            for cx, cy, r1, r2 in circles:
                all_circles.append((cx + x, cy + y, r1, r2))

    return all_circles
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Now segmentation will print debug info
segmenter = MushroomSegmenter(Settings())
circles = segmenter.segment(image)
```
