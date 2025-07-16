"""Settings module for mushroom segmentation application."""
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # Segmentation parameters
    back_threshold: int = Field(
        default=100, ge=0, le=255, description="Threshold for background segmentation"
    )

    threshold: int = Field(
        default=150, ge=0, le=255, description="Threshold for object segmentation"
    )

    min_diameter: int = Field(
        default=30, ge=1, description="Minimum diameter for object detection in pixels"
    )

    peaks_rel_threshold: float = Field(
        default=0.1, ge=0.0, le=1.0, description="Relative threshold for peak detection"
    )

    # Image processing parameters
    gaussian_kernel_size: int = Field(default=5, description="Size of Gaussian blur kernel")

    clahe_clip_limit: float = Field(
        default=2.0, ge=0.0, description="CLAHE clip limit for histogram equalization"
    )

    clahe_tile_size: int = Field(default=8, ge=1, description="CLAHE tile grid size")

    morphology_kernel_size: int = Field(
        default=3, ge=1, description="Size of morphological operations kernel"
    )

    # Visualization parameters
    center_color: tuple[int, int, int] = Field(
        default=(255, 0, 0), description="Color for circle centers (BGR)"
    )

    radius1_color: tuple[int, int, int] = Field(
        default=(0, 255, 0), description="Color for first radius (BGR)"
    )

    radius2_color: tuple[int, int, int] = Field(
        default=(0, 0, 255), description="Color for second radius (BGR)"
    )

    line_thickness: int = Field(default=2, ge=1, description="Line thickness for drawing circles")

    @field_validator("gaussian_kernel_size", "morphology_kernel_size")
    def validate_odd_kernel_size(cls, v: int) -> int:
        """Ensure kernel sizes are odd numbers."""
        if v % 2 == 0:
            return v + 1
        return v
