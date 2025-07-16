"""Advanced segmentation algorithm for mushroom detection."""
import logging
from typing import List, Tuple

import cv2
import numpy as np
from skimage.feature import corner_peaks

from ..config.settings import Settings

logger = logging.getLogger(__name__)


class MushroomSegmenter:
    """
    Advanced segmentation algorithm for detecting circular objects in images.

    This class implements a multi-stage image processing pipeline optimized
    for detecting mushrooms and other circular objects in various lighting
    conditions.
    """

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the segmenter with configuration settings.

        Args:
            settings: Configuration settings for the segmentation algorithm
        """
        self.settings = settings
        self._clahe = cv2.createCLAHE(
            clipLimit=settings.clahe_clip_limit,
            tileGridSize=(settings.clahe_tile_size, settings.clahe_tile_size),
        )

    def segment(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Perform segmentation on the input image.

        Args:
            image: Input image as numpy array (BGR format)

        Returns:
            List of detected circles as (x, y, radius1, radius2) tuples
        """
        logger.debug("Starting segmentation process")

        # Preprocessing
        preprocessed = self._preprocess_image(image)

        # Background removal
        foreground_mask = self._remove_background(preprocessed)

        # Apply mask to preprocessed image
        masked_image = cv2.bitwise_and(preprocessed, preprocessed, mask=foreground_mask)

        # Distance transform
        dist_map = self._compute_distance_transform(masked_image)

        # Histogram equalization for better peak detection
        equalized_image = self._clahe.apply(masked_image)
        equalized_dist_map = self._compute_distance_transform(equalized_image)

        # Find local maxima
        peaks = self._find_local_maxima(equalized_dist_map)

        # Extract circles
        circles = self._extract_circles(peaks, dist_map, equalized_dist_map)

        logger.info(f"Segmentation complete. Found {len(circles)} objects")
        return circles

    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Apply preprocessing steps to the image."""
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(
            image, (self.settings.gaussian_kernel_size, self.settings.gaussian_kernel_size), 0
        )

        # Convert to grayscale
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE for normalization
        normalized = self._clahe.apply(gray)

        return normalized

    def _remove_background(self, image: np.ndarray) -> np.ndarray:
        """Remove background using threshold and morphological operations."""
        # Threshold
        _, binary = cv2.threshold(image, self.settings.back_threshold, 255, cv2.THRESH_BINARY)

        # Morphological operations
        kernel = np.ones(
            (self.settings.morphology_kernel_size, self.settings.morphology_kernel_size), np.uint8
        )

        # Opening to remove small objects
        iterations = max(1, self.settings.min_diameter // 3)
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=iterations)

        # Dilation to connect nearby regions
        dilated = cv2.dilate(opened, kernel, iterations=5)

        return dilated

    def _compute_distance_transform(self, image: np.ndarray) -> np.ndarray:
        """Compute distance transform of the binary image."""
        # Threshold if not already binary
        if len(np.unique(image)) > 2:
            _, binary = cv2.threshold(image, self.settings.threshold, 255, cv2.THRESH_BINARY)
        else:
            binary = image

        # Compute distance transform
        dist = cv2.distanceTransform(binary, cv2.DIST_L2, 3)

        return dist

    def _find_local_maxima(self, distance_map: np.ndarray) -> np.ndarray:
        """Find local maxima in the distance map."""
        peaks = corner_peaks(
            distance_map,
            min_distance=self.settings.min_diameter,
            threshold_rel=self.settings.peaks_rel_threshold,
            indices=True,
        )

        logger.debug(f"Found {len(peaks)} local maxima")
        return peaks

    def _extract_circles(
        self, peaks: np.ndarray, dist_map: np.ndarray, equalized_dist_map: np.ndarray
    ) -> List[Tuple[int, int, int, int]]:
        """Extract circle parameters from peak locations."""
        circles = []

        # Calculate compensation coefficient
        coeff = 1 + (self.settings.threshold - self.settings.back_threshold) / (
            255 - self.settings.back_threshold
        )

        for peak in peaks:
            y, x = peak

            # Get radii from both distance maps
            radius1 = int(dist_map[y, x] * coeff)
            radius2 = int(equalized_dist_map[y, x] * coeff)

            # Filter by minimum diameter
            if radius1 >= self.settings.min_diameter // 2:
                circles.append((x, y, radius1, radius2))

        return circles
