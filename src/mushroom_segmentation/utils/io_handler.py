"""Image I/O and Results Exporter Module."""
import csv
import logging
from pathlib import Path
from typing import List, Tuple, Union

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class ImageIO:
    """Handle image input/output operations."""

    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}

    @classmethod
    def load_image(cls, path: Union[str, Path]) -> np.ndarray:
        """
        Load an image from file.

        Args:
            path: Path to the image file

        Returns:
            Image as numpy array in BGR format

        Raises:
            ValueError: If image format is not supported
            RuntimeError: If image cannot be loaded
        """
        path = Path(path)

        if path.suffix.lower() not in cls.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported image format: {path.suffix}. "
                f"Supported formats: {', '.join(cls.SUPPORTED_FORMATS)}"
            )

        image = cv2.imread(str(path))

        if image is None:
            raise RuntimeError(f"Failed to load image: {path}")

        logger.debug(f"Loaded image: {path} (shape: {image.shape})")
        return image

    @classmethod
    def save_image(cls, image: np.ndarray, path: Union[str, Path]) -> None:
        """
        Save an image to file.

        Args:
            image: Image array to save
            path: Output file path

        Raises:
            RuntimeError: If image cannot be saved
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        success = cv2.imwrite(str(path), image)

        if not success:
            raise RuntimeError(f"Failed to save image: {path}")

        logger.debug(f"Saved image: {path}")


class ResultsExporter:
    """Export segmentation results in various formats."""

    @staticmethod
    def to_csv(
        circles: List[Tuple[int, int, int, int]], path: Union[str, Path], header: bool = True
    ) -> None:
        """
        Export circles to CSV file.

        Args:
            circles: List of circles as (x, y, radius1, radius2) tuples
            path: Output CSV file path
            header: Whether to include header row
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)

            if header:
                writer.writerow(["X", "Y", "Radius_1", "Radius_2"])

            writer.writerows(circles)

        logger.debug(f"Exported {len(circles)} circles to {path}")

    @staticmethod
    def to_json(
        circles: List[Tuple[int, int, int, int]], path: Union[str, Path], metadata: dict = None
    ) -> None:
        """
        Export circles to JSON file with optional metadata.

        Args:
            circles: List of circles
            path: Output JSON file path
            metadata: Optional metadata to include
        """
        import json

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "circles": [
                {"x": x, "y": y, "radius_1": r1, "radius_2": r2} for x, y, r1, r2 in circles
            ],
            "count": len(circles),
        }

        if metadata:
            data["metadata"] = metadata

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        logger.debug(f"Exported results to JSON: {path}")
