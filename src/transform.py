import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

TEXT_COLUMNS = ["artists", "album_name", "track_name", "track_genre"]


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove fully duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    logger.info(f"Removed {before - after} duplicate rows")
    return df


def remove_duplicate_track_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with duplicate track_id, keeping the first occurrence."""
    before = len(df)
    df = df.drop_duplicates(subset=["track_id"], keep="first")
    after = len(df)
    logger.info(f"Removed {before - after} duplicate track_id values")
    return df


def strip_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from text columns."""
    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    logger.info("Stripped whitespace from text columns")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with any missing values and log the count."""
    before = len(df)
    df = df.dropna()
    after = len(df)
    logger.info(f"Dropped {before - after} rows with missing values")
    return df


def lower_case_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert all column names to lowercase."""
    df.columns = [col.lower() for col in df.columns]
    logger.info("Converted column names to lowercase")
    return df


def validate_numerical_ranges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and filter rows that fall outside expected numerical ranges.

    Removes rows where:
    - popularity is not between 0 and 100
    - danceability, energy, speechiness, acousticness, instrumentalness,
      liveness, valence are not between 0 and 1
    - duration_ms <= 0
    - tempo <= 0
    """
    before = len(df)

    df = df[(df["popularity"] >= 0) & (df["popularity"] <= 100)]
    range_0_1_cols = [
        "danceability", "energy", "speechiness",
        "acousticness", "instrumentalness", "liveness", "valence"
    ]
    for col in range_0_1_cols:
        df = df[(df[col] >= 0) & (df[col] <= 1)]

    df = df[df["duration_ms"] > 0]
    df = df[df["tempo"] > 0]
    df = df[pd.to_numeric(df["loudness"], errors="coerce").notna()]

    after = len(df)
    logger.info(f"Removed {before - after} rows failing numerical validation")
    return df


def convert_explicit_to_bool(df: pd.DataFrame) -> pd.DataFrame:
    """Convert explicit column to boolean (True/False)."""
    if "explicit" in df.columns:
        df["explicit"] = df["explicit"].astype(bool)
        logger.info("Converted explicit column to boolean")
    return df


def create_duration_min(df: pd.DataFrame) -> pd.DataFrame:
    """Create duration_min from duration_ms."""
    df["duration_min"] = df["duration_ms"] / 60000.0
    logger.info("Created duration_min feature")
    return df


def create_popularity_category(df: pd.DataFrame) -> pd.DataFrame:
    """Categorize popularity into Low, Medium, High."""
    def categorize(pop):
        if pop <= 30:
            return "Low"
        elif pop <= 70:
            return "Medium"
        else:
            return "High"

    df["popularity_category"] = df["popularity"].apply(categorize)
    logger.info("Created popularity_category feature")
    return df


def create_energy_level(df: pd.DataFrame) -> pd.DataFrame:
    """Categorize energy into Low, Medium, High."""
    def categorize(val):
        if val <= 0.4:
            return "Low"
        elif val <= 0.7:
            return "Medium"
        else:
            return "High"

    df["energy_level"] = df["energy"].apply(categorize)
    logger.info("Created energy_level feature")
    return df


def create_danceability_level(df: pd.DataFrame) -> pd.DataFrame:
    """Categorize danceability into Low, Medium, High."""
    def categorize(val):
        if val <= 0.4:
            return "Low"
        elif val <= 0.7:
            return "Medium"
        else:
            return "High"

    df["danceability_level"] = df["danceability"].apply(categorize)
    logger.info("Created danceability_level feature")
    return df


def create_mood_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize tracks into mood categories based on valence and energy.

    Rules:
    - Happy/Energetic: valence >= 0.6 and energy >= 0.6
    - Calm: valence >= 0.4 and energy < 0.6
    - Sad/Low Energy: valence < 0.4 and energy < 0.5
    - Intense: valence < 0.5 and energy >= 0.7
    - Neutral: everything else
    """
    def categorize(row):
        valence = row["valence"]
        energy = row["energy"]
        if valence >= 0.6 and energy >= 0.6:
            return "Happy/Energetic"
        elif valence >= 0.4 and energy < 0.6:
            return "Calm"
        elif valence < 0.4 and energy < 0.5:
            return "Sad/Low Energy"
        elif valence < 0.5 and energy >= 0.7:
            return "Intense"
        else:
            return "Neutral"

    df["mood_category"] = df.apply(categorize, axis=1)
    logger.info("Created mood_category feature")
    return df


def save_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned DataFrame to a CSV file."""
    df.to_csv(output_path, index=False)
    logger.info(f"Cleaned data saved to: {output_path}")


def transform_data(df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    """
    Apply all cleaning and transformation steps to the raw DataFrame.

    Args:
        df (pd.DataFrame): Raw DataFrame from extraction step.
        output_path (str): Path to save the cleaned CSV.

    Returns:
        pd.DataFrame: Transformed and cleaned DataFrame.
    """
    logger.info("Starting data transformation")

    df = lower_case_columns(df)
    df = remove_duplicates(df)
    df = remove_duplicate_track_ids(df)
    df = strip_text_columns(df)
    df = handle_missing_values(df)
    df = validate_numerical_ranges(df)
    df = convert_explicit_to_bool(df)

    # Feature engineering
    df = create_duration_min(df)
    df = create_popularity_category(df)
    df = create_energy_level(df)
    df = create_danceability_level(df)
    df = create_mood_category(df)

    logger.info(f"Transformation complete: {len(df)} rows in final dataset")
    save_cleaned_data(df, output_path)
    return df
