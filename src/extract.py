import pandas as pd
import logging

logger = logging.getLogger(__name__)


def extract_data(file_path: str) -> pd.DataFrame:
    """
    Extract Spotify track data from a CSV file.

    Reads the CSV file into a pandas DataFrame and logs basic info.

    Args:
        file_path (str): Path to the raw CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the raw data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    try:
        logger.info(f"Starting data extraction from: {file_path}")
        df = pd.read_csv(file_path)
        rows, cols = df.shape
        logger.info(f"Extraction complete: {rows} rows and {cols} columns loaded")
        return df
    except FileNotFoundError:
        logger.error(f"File not found at path: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error during extraction: {e}")
        raise
