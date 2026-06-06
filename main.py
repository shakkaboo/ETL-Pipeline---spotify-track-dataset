import logging
import schedule
import time
import sys
from src.spotify_api import extract_tracks_from_api
from src.load_api import load_api_data

from src.pipeline import run_etl_pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


def schedule_daily(time_str: str) -> None:
    """
    Schedule the ETL pipeline to run daily at a given time.

    Args:
        time_str (str): Time in HH:MM format (24-hour).
    """
    schedule.every().day.at(time_str).do(run_etl_pipeline)
    logger.info(f"ETL pipeline scheduled to run daily at {time_str}")
    print(f"\nPipeline will run daily at {time_str}. Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(30)


def run_spotify_api_pipeline():
    queries = ["pop", "rock", "hip hop", "classical", "edm", "tamil", "japanese"]

    df = extract_tracks_from_api(
        queries=queries,
        limit=10,
    )

    load_api_data(df)

    print("Spotify API ETL pipeline completed successfully.")


def main():
    while True:
        print("\nSpotify ETL Pipeline")
        print("1. Run Kaggle CSV ETL pipeline")
        print("2. Run Spotify API ETL pipeline")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            run_etl_pipeline()
        elif choice == "2":
            run_spotify_api_pipeline()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
