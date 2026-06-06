# Spotify Tracks ETL Pipeline

A complete ETL (Extract, Transform, Load) pipeline that processes Spotify track data from CSV, cleans and transforms it, stores it in PostgreSQL, and provides SQL queries for analysis.

## Dataset

This project uses the **Spotify Tracks Dataset** from Kaggle:

https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset

The dataset contains ~114,000 tracks with audio features like danceability, energy, tempo, valence, and more.

### Columns in the dataset

track_id, artists, album_name, track_name, popularity, duration_ms, explicit, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, track_genre

## Tech Stack

- **Python 3.10+**
- **Pandas** - Data manipulation and CSV reading
- **NumPy** - Numerical operations
- **PostgreSQL** - Data warehouse / storage
- **SQLAlchemy** - Database connection and ORM
- **psycopg2-binary** - PostgreSQL driver for Python
- **python-dotenv** - Environment variable management
- **schedule** - Pipeline scheduling
- **logging** - Built-in logging module

## Folder Structure

```
spotify-etl-pipeline/
│
├── data/
│   ├── raw/
│   │   └── spotify_tracks.csv        # Raw input file (download from Kaggle)
│   └── processed/
│       └── spotify_tracks_cleaned.csv # Cleaned output after transformation
│
├── src/
│   ├── extract.py                     # Extracts data from CSV
│   ├── transform.py                   # Cleans and transforms data
│   ├── load.py                        # Loads data into PostgreSQL
│   ├── pipeline.py                    # Orchestrates ETL steps
│   └── db_config.py                   # Database connection config
│
├── sql/
│   ├── create_tables.sql              # SQL to create the table
│   └── analysis_queries.sql           # Analysis queries for insights
│
├── logs/
│   └── pipeline.log                   # Pipeline execution logs
│
├── .env.example                       # Environment variable template
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
└── main.py                            # Entry point with CLI menu
```

## Setup Instructions

### 1. Clone / Download the Project

```bash
cd spotify-etl-pipeline
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate    # Linux / macOS
# OR
venv\Scripts\activate       # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the Dataset from Kaggle

1. Go to: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
2. Click the **Download** button
3. Extract the ZIP file
4. Find `dataset.csv` (or `spotify_tracks.csv`)
5. Copy it to: `data/raw/spotify_tracks.csv`

### 5. Create PostgreSQL Database

Open your PostgreSQL terminal (psql) or use a GUI like pgAdmin:

```sql
CREATE DATABASE spotify_db;
```

### 6. Create the .env File

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=spotify_db
DB_USER=postgres
DB_PASSWORD=your_actual_password
```

### 7. (Optional) Create the Table Manually

```bash
psql -U postgres -d spotify_db -f sql/create_tables.sql
```

The pipeline will create the table automatically when it runs, so this step is optional.

## How to Run the Pipeline

### Run Once

```bash
python main.py
```

Then select option **1** from the menu.

### Schedule Daily

```bash
python main.py
```

Select option **2** and enter a time in HH:MM format (e.g., `08:00`).

The pipeline will run daily at that time using the `schedule` library.

### Run SQL Analysis Queries

After loading data into PostgreSQL, connect to your database and run:

```bash
psql -U postgres -d spotify_db -f sql/analysis_queries.sql
```

Or open the SQL file in pgAdmin and run individual queries.

## What Each File Does

### extract.py

Reads the raw CSV file (`data/raw/spotify_tracks.csv`) using `pandas.read_csv()`. It logs the number of rows and columns loaded. If the file is missing, it raises a clear error.

### transform.py

The heart of the pipeline. It performs:

- **Lowercase columns** - all column names are converted to lowercase for consistency
- **Remove duplicates** - drops fully duplicate rows and duplicate track_id values
- **Strip whitespace** - removes leading/trailing spaces from text fields (artists, album_name, track_name, track_genre)
- **Handle missing values** - drops rows with any null values
- **Validate numerical ranges** - ensures data integrity:
  - popularity: 0 to 100
  - danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence: 0 to 1
  - duration_ms > 0
  - tempo > 0
  - loudness must be numeric
- **Convert explicit to boolean** - converts the explicit column to True/False

**Feature Engineering:**
- `duration_min` = duration_ms / 60000 (convert milliseconds to minutes)
- `popularity_category`: Low (0-30), Medium (31-70), High (71-100)
- `energy_level`: Low (0-0.4), Medium (0.4-0.7), High (0.7-1.0)
- `danceability_level`: Low (0-0.4), Medium (0.4-0.7), High (0.7-1.0)
- `mood_category`:
  - Happy/Energetic: high valence + high energy
  - Calm: medium valence + low energy
  - Sad/Low Energy: low valence + low energy
  - Intense: low valence + high energy
  - Neutral: everything else

The cleaned data is saved to `data/processed/spotify_tracks_cleaned.csv`.

### load.py

Connects to PostgreSQL using SQLAlchemy and loads the cleaned DataFrame into a table called `spotify_tracks_cleaned`. Uses `if_exists="replace"` so it overwrites the table each time the pipeline runs. Logs the number of rows inserted.

### db_config.py

Reads database credentials from the `.env` file using `python-dotenv` and builds a PostgreSQL connection URL for SQLAlchemy.

### pipeline.py

Orchestrates the full ETL process by calling extract → transform → load in sequence. Each step is wrapped in try/except blocks with clear logging.

### main.py

The entry point. Provides a simple menu:
1. Run ETL once
2. Schedule daily runs (using the `schedule` library)
3. Exit

## How Data Flows

```
CSV File (data/raw/spotify_tracks.csv)
    │
    ▼
extract.py  ──► pandas DataFrame (raw data)
    │
    ▼
transform.py ──► Cleaned DataFrame
    │                  │
    │                  ▼
    │         CSV saved to
    │    data/processed/spotify_tracks_cleaned.csv
    │
    ▼
load.py ──► PostgreSQL table: spotify_tracks_cleaned
    │
    ▼
Analysis ──► SQL queries in sql/analysis_queries.sql
```

## How PostgreSQL Connection Works

1. `db_config.py` reads `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` from `.env`
2. It builds a connection URL: `postgresql://user:password@host:port/dbname`
3. `load.py` uses SQLAlchemy's `create_engine(db_url)` to connect
4. `df.to_sql()` writes the entire DataFrame to the PostgreSQL table
5. A count query verifies the insertion was successful

## How Scheduling Works

The `schedule` library checks the current time every 30 seconds. When the configured time matches, it runs the `run_etl_pipeline()` function. The pipeline continues running in the background until you press Ctrl+C.

## Future Improvements

- **Apache Airflow** - Replace the simple scheduler with Airflow DAGs for production-grade orchestration with retries, monitoring, and dependency management
- **Docker** - Containerize the entire pipeline with Docker and Docker Compose for easy deployment
- **Spotify API Ingestion** - Replace CSV reading with live data from the Spotify Web API for real-time updates
- **Power BI Dashboard** - Connect PostgreSQL to Power BI for interactive visualizations and dashboards
- **ML Popularity Prediction Model** - Use the numerical features to build a machine learning model that predicts track popularity

## License

This project is for educational purposes. The dataset is from Kaggle and subject to its license terms.
