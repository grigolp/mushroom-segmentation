"""Visualizer module for mushroom segmentation application."""
import logging
from typing import List, Optional, Tuple

import cv2
import numpy as np

from ..config.settings import Settings

logger = logging.getLogger(__name__)


class Visualizer:
    """Handle visualization of segmentation results."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        """
        Initialize visualizer with optional settings.

        Args:
            settings: Configuration settings for visualization
        """
        self.settings = settings or Settings()

    def draw_circles(
        self, image: np.ndarray, circles: List[Tuple[int, int, int, int]], copy: bool = True
    ) -> np.ndarray:
        """
        Draw detected circles on the image.

        Args:
            image: Input image
            circles: List of circles as (x, y, radius1, radius2) tuples
            copy: Whether to copy the image before drawing

        Returns:
            Image with circles drawn
        """
        if copy:
            image = image.copy()

        for x, y, radius1, radius2 in circles:
            # Draw center point
            cv2.circle(image, (x, y), 3, self.settings.center_color, -1)

            # Draw first radius (green)
            cv2.circle(
                image, (x, y), radius1, self.settings.radius1_color, self.settings.line_thickness
            )

            # Draw second radius (red) - from histogram equalized image
            cv2.circle(
                image, (x, y), radius2, self.settings.radius2_color, self.settings.line_thickness
            )

        return image

    def create_overlay(
        self, image: np.ndarray, circles: List[Tuple[int, int, int, int]], alpha: float = 0.3
    ) -> np.ndarray:
        """
        Create an overlay visualization with semi-transparent circles.

        Args:
            image: Input image
            circles: List of circles
            alpha: Transparency factor (0-1)

        Returns:
            Image with overlay
        """
        overlay = image.copy()
        output = image.copy()

        for x, y, _, radius2 in circles:
            cv2.circle(overlay, (x, y), radius2, self.settings.radius2_color, -1)

        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

        # Draw circle borders
        output = self.draw_circles(output, circles, copy=False)

        return output

    def display(
        self, image: np.ndarray, window_name: str = "Segmentation Results", wait: bool = True
    ) -> None:
        """
        Display image in a window.

        Args:
            image: Image to display
            window_name: Name of the display window
            wait: Whether to wait for key press
        """
        cv2.imshow(window_name, image)

        if wait:
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def create_comparison(
        self, original: np.ndarray, processed: np.ndarray, orientation: str = "horizontal"
    ) -> np.ndarray:
        """
        Create a side-by-side comparison of original and processed images.

        Args:
            original: Original image
            processed: Processed image with annotations
            orientation: "horizontal" or "vertical"

        Returns:
            Combined comparison image
        """
        if orientation == "horizontal":
            comparison = np.hstack([original, processed])
        else:
            comparison = np.vstack([original, processed])

        return comparison
