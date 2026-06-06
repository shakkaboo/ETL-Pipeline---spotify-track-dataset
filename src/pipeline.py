import logging
import os

from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

logger = logging.getLogger(__name__)

RAW_DATA_PATH = "data/raw/spotify_tracks.csv"
PROCESSED_DATA_PATH = "data/processed/spotify_tracks_cleaned.csv"


def run_etl_pipeline() -> None:
    """
    Execute the complete ETL pipeline: Extract → Transform → Load.

    Steps:
        1. Extract raw data from CSV.
        2. Clean, validate, and transform the data.
        3. Save cleaned CSV locally.
        4. Load cleaned data into PostgreSQL.

    Logs success or failure at each stage.
    """
    logger.info("=" * 50)
    logger.info("ETL PIPELINE STARTED")
    logger.info("=" * 50)

    try:
        # Step 1: Extract
        logger.info("--- EXTRACT STEP ---")
        raw_df = extract_data(RAW_DATA_PATH)

        # Step 2: Transform
        logger.info("--- TRANSFORM STEP ---")
        os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
        cleaned_df = transform_data(raw_df, PROCESSED_DATA_PATH)

        # Step 3: Load
        logger.info("--- LOAD STEP ---")
        load_data(cleaned_df)

        logger.info("=" * 50)
        logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 50)

    except FileNotFoundError:
        logger.error(
            "CSV file not found. Please place 'spotify_tracks.csv' in the "
            "data/raw/ directory."
        )
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise
