"""Validators for Mushroom Segmentation Application."""
from pathlib import Path
from typing import Union


def validate_image_path(path: Union[str, Path]) -> Path:
    """
    Validate image file path.

    Args:
        path: Path to validate

    Returns:
        Validated Path object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not an image
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}
    if path.suffix.lower() not in valid_extensions:
        raise ValueError(
            f"Invalid image format: {path.suffix}. "
            f"Supported formats: {', '.join(valid_extensions)}"
        )

    return path


def validate_output_path(path: Union[str, Path]) -> Path:
    """
    Validate output file path.

    Args:
        path: Path to validate

    Returns:
        Validated Path object

    Raises:
        ValueError: If path is invalid
    """
    path = Path(path)

    # Check if parent directory can be created
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise ValueError(f"Cannot create output directory: {e}")

    return path


def validate_parameters(settings: dict) -> dict:
    """
    Validate segmentation parameters.

    Args:
        settings: Dictionary of parameters

    Returns:
        Validated parameters

    Raises:
        ValueError: If parameters are invalid
    """
    validated = {}

    # Validate thresholds
    for key in ["back_threshold", "threshold"]:
        if key in settings:
            value = settings[key]
            if not isinstance(value, int) or not 0 <= value <= 255:
                raise ValueError(f"{key} must be an integer between 0 and 255")
            validated[key] = value

    # Validate min_diameter
    if "min_diameter" in settings:
        value = settings["min_diameter"]
        if not isinstance(value, int) or value < 1:
            raise ValueError("min_diameter must be a positive integer")
        validated["min_diameter"] = value

    # Validate peaks_rel_threshold
    if "peaks_rel_threshold" in settings:
        value = settings["peaks_rel_threshold"]
        if not isinstance(value, (int, float)) or not 0 <= value <= 1:
            raise ValueError("peaks_rel_threshold must be between 0 and 1")
        validated["peaks_rel_threshold"] = float(value)

    return validated
