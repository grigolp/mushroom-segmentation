# Algorithm Documentation

## Overview

The mushroom segmentation algorithm uses a multi-stage image processing pipeline optimized for detecting circular objects under varying lighting conditions.

## Pipeline Stages

### 1. Preprocessing

- **Gaussian Blur**: Reduces noise while preserving edges
- **Grayscale Conversion**: Simplifies processing
- **CLAHE**: Contrast Limited Adaptive Histogram Equalization normalizes lighting

### 2. Background Removal

- **Thresholding**: Separates foreground objects from background
- **Morphological Opening**: Removes small noise artifacts
- **Dilation**: Connects nearby regions

### 3. Distance Transform

- Computes distance from each foreground pixel to nearest background
- Creates "peaks" at object centers
- Applied to both original and histogram-equalized images

### 4. Peak Detection

- Uses `corner_peaks` from scikit-image
- Finds local maxima in distance map
- Filters by minimum distance and relative threshold

### 5. Circle Extraction

- Extracts circle parameters from peak locations
- Calculates two radii:
  - Radius 1: From standard distance transform
  - Radius 2: From histogram-equalized distance transform
- Applies compensation coefficient for threshold effects

## Parameters

### Critical Parameters

1. **back_threshold**: Controls background segmentation sensitivity
   - Lower values: More inclusive background removal
   - Higher values: More selective, may miss dim objects

2. **threshold**: Controls object boundary detection
   - Lower values: Larger detected radii
   - Higher values: Smaller, more conservative radii

3. **min_diameter**: Minimum object size filter
   - Prevents detection of noise as objects
   - Should match smallest expected mushroom size

4. **peaks_rel_threshold**: Peak detection sensitivity
   - Lower values: More peaks detected
   - Higher values: Only strongest peaks selected

### Fine-tuning Parameters

1. **gaussian_kernel_size**: Blur strength
   - Larger values: More smoothing, better for noisy images
   - Must be odd number

2. **clahe_clip_limit**: Contrast enhancement strength
   - Higher values: More aggressive equalization
   - May introduce artifacts if too high

3. **clahe_tile_size**: Local region size for equalization
   - Smaller values: More localized enhancement
   - Larger values: More global enhancement

## Performance Considerations

### Time Complexity

- Preprocessing: O(n) where n = image pixels
- Distance Transform: O(n)
- Peak Detection: O(p log p) where p = number of peaks
- Overall: O(n) for typical images

### Memory Usage

- Requires ~5x input image size in memory
- Includes: original, grayscale, masks, distance maps

### Optimization Tips

1. **Resize large images** before processing if exact measurements not required
2. **Adjust min_diameter** to filter early in pipeline
3. **Use lower peaks_rel_threshold** for sparse images

## Common Issues and Solutions

### Issue: Missing detections

**Solutions:**
- Decrease `back_threshold`
- Decrease `peaks_rel_threshold`
- Check if objects meet `min_diameter`

### Issue: False positives

**Solutions:**
- Increase `peaks_rel_threshold`
- Increase `min_diameter`
- Adjust morphological operations

### Issue: Incorrect radius

**Solutions:**
- Fine-tune `threshold` parameter
- Check compensation coefficient
- Use appropriate radius (1 or 2) for your use case

## Algorithm Limitations

1. **Shape Assumption**: Assumes circular/elliptical objects
2. **Overlap Handling**: May merge heavily overlapping objects
3. **Contrast Requirement**: Needs sufficient contrast between object and background
4. **Size Variation**: Very large size variations may require parameter adjustment
