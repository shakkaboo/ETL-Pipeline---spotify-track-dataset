import pandas as pd
from sqlalchemy import create_engine, text
import logging

from src.db_config import get_db_url

logger = logging.getLogger(__name__)


def load_data(df: pd.DataFrame, table_name: str = "spotify_tracks_cleaned") -> None:
    """
    Load cleaned DataFrame into PostgreSQL table.

    Connects to PostgreSQL using credentials from .env file,
    creates the table if it doesn't exist, and inserts the data.

    Args:
        df (pd.DataFrame): Cleaned DataFrame to load.
        table_name (str): Name of the target table.
    """
    try:
        db_url = get_db_url()
        engine = create_engine(db_url)
        logger.info(f"Connected to PostgreSQL database")

        df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)

        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            row_count = result.scalar()

        logger.info(f"Successfully loaded {row_count} rows into table '{table_name}'")
        engine.dispose()

    except Exception as e:
        logger.error(f"Error loading data into PostgreSQL: {e}")
        raise
