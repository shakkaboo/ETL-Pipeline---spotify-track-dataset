import os
from dotenv import load_dotenv

load_dotenv()


def get_db_url() -> str:
    """
    Build and return a PostgreSQL connection URL from environment variables.

    Reads DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD from .env file.
    Falls back to default values if not set.

    Returns:
        str: SQLAlchemy connection URL for PostgreSQL.
    """
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "spotify_db")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "your_password")

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"
