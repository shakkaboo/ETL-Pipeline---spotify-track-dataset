from sqlalchemy import create_engine
from src.db_config import get_db_url


def load_api_data(df, table_name="spotify_tracks_api"):
    engine = create_engine(get_db_url())

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
    )

    print(f"Loaded {len(df)} API records into table: {table_name}")