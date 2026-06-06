import logging
import schedule
import time
import sys

from src.pipeline import run_etl_pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
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


def main():
    """Display menu and handle user choices."""
    while True:
        print("\n" + "=" * 50)
        print("   SPOTIFY TRACKS ETL PIPELINE")
        print("=" * 50)
        print("1. Run ETL pipeline once")
        print("2. Schedule ETL pipeline daily")
        print("3. Exit")
        print("=" * 50)

        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice == "1":
            print("\nRunning ETL pipeline...")
            run_etl_pipeline()
            print("\nETL pipeline finished! Check logs/pipeline.log for details.")

        elif choice == "2":
            time_input = input("Enter time to run daily (HH:MM, 24-hour format): ").strip()
            try:
                schedule_daily(time_input)
            except (ValueError, IndexError):
                print("Invalid time format. Please use HH:MM (e.g., 08:00, 14:30).")

        elif choice == "3":
            print("Exiting. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
