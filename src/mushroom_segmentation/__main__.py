"""Main entry point for the Mushroom Segmentation application."""
import logging
import sys
from pathlib import Path
from typing import Optional

import click

from .config.settings import Settings
from .core.segmentation import MushroomSegmenter
from .core.visualization import Visualizer
from .utils.io_handler import ImageIO, ResultsExporter
from .utils.validators import validate_image_path, validate_output_path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("input_image", type=click.Path(exists=True))
@click.option(
    "--output-csv", "-o", default="results.csv", help="Output CSV file path", type=click.Path()
)
@click.option("--visualize/--no-visualize", default=True, help="Display visualization of results")
@click.option("--save-visualization", "-s", help="Save visualization to file", type=click.Path())
@click.option("--config", "-c", help="Configuration file path", type=click.Path(exists=True))
@click.option(
    "--back-threshold",
    default=100,
    help="Background threshold value (0-255)",
    type=click.IntRange(0, 255),
)
@click.option(
    "--threshold",
    default=150,
    help="Segmentation threshold value (0-255)",
    type=click.IntRange(0, 255),
)
@click.option(
    "--min-diameter",
    default=30,
    help="Minimum diameter for detection (pixels)",
    type=click.IntRange(1, None),
)
@click.option(
    "--peaks-threshold",
    default=0.1,
    help="Relative threshold for peak detection (0-1)",
    type=click.FloatRange(0, 1),
)
def cli(
    input_image: str,
    output_csv: str,
    visualize: bool,
    save_visualization: Optional[str],
    config: Optional[str],
    back_threshold: int,
    threshold: int,
    min_diameter: int,
    peaks_threshold: float,
) -> None:
    """
    Detect and segment circular objects (mushrooms) in images.

    INPUT_IMAGE: Path to the input image file (JPG or PNG)
    """
    try:
        # Load configuration
        settings = Settings()
        if config:
            settings = Settings(_env_file=config)

        # Override with CLI arguments if provided
        settings.back_threshold = back_threshold
        settings.threshold = threshold
        settings.min_diameter = min_diameter
        settings.peaks_rel_threshold = peaks_threshold

        # Validate paths
        input_path = validate_image_path(input_image)
        output_path = validate_output_path(output_csv)

        logger.info(f"Processing image: {input_path}")

        # Load image
        image_io = ImageIO()
        image = image_io.load_image(input_path)

        # Perform segmentation
        segmenter = MushroomSegmenter(settings)
        results = segmenter.segment(image)

        logger.info(f"Detected {len(results)} objects")

        # Export results
        exporter = ResultsExporter()
        exporter.to_csv(results, output_path)
        logger.info(f"Results saved to: {output_path}")

        # Visualization
        if visualize or save_visualization:
            visualizer = Visualizer()
            annotated_image = visualizer.draw_circles(image, results)

            if save_visualization:
                vis_path = Path(save_visualization)
                image_io.save_image(annotated_image, vis_path)
                logger.info(f"Visualization saved to: {vis_path}")

            if visualize:
                visualizer.display(annotated_image, window_name="Mushroom Segmentation Results")

        logger.info("Processing completed successfully")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
