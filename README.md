# Spotify Analytics Platform: ETL, Dashboard & Popularity Prediction

## Project Overview

An end-to-end Spotify Data Engineering and Machine Learning project that ingests Spotify music data from both a Kaggle dataset and the Spotify Web API, performs ETL processing, stores transformed data in PostgreSQL, visualizes insights through Streamlit dashboards, and predicts song popularity using Machine Learning.

This project demonstrates:

* Data Engineering (ETL)
* Database Management (PostgreSQL)
* Feature Engineering
* Machine Learning
* Data Visualization
* Interactive Dashboard Development

---

## Architecture

```text
Spotify API              Kaggle Dataset
      │                        │
      └──────────┬─────────────┘
                 │
                 ▼
           ETL Pipeline
                 │
                 ▼
            PostgreSQL
                 │
       ┌─────────┴─────────┐
       │                   │
       ▼                   ▼
 Streamlit Dashboard   ML Training
       │                   │
       ▼                   ▼
 Analytics         Popularity Prediction
```

---

## Dataset

Spotify Tracks Dataset from Kaggle:

https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset

Dataset Size:

* ~114,000 tracks
* Multiple genres
* Audio features
* Popularity metrics

Features include:

* Danceability
* Energy
* Tempo
* Valence
* Acousticness
* Speechiness
* Instrumentalness
* Loudness
* Popularity
* Genre
* Explicit content

---

## Features

### ETL Pipeline

* Extract Spotify track data
* Clean and validate records
* Remove duplicates
* Handle missing values
* Feature engineering
* Store processed data in PostgreSQL

### Spotify API Integration

Fetch live Spotify track data using:

* Client Credentials Flow
* Spotify Search API
* Multiple search categories
* Automatic PostgreSQL loading

### PostgreSQL Data Warehouse

Stores:

* Cleaned Kaggle dataset
* Spotify API dataset
* Engineered features
* ML-ready data

### Interactive Streamlit Dashboard

Dashboard includes:

* KPI Cards
* Genre Analytics
* Artist Analytics
* Popularity Distribution
* Audio Feature Analysis
* Correlation Analysis
* Search and Filtering
* Top Songs Analysis

### Machine Learning

Predict song popularity using:

* Random Forest Regressor
* Feature Engineering
* Genre Encoding
* Model Evaluation

---

## Technology Stack

### Backend

* Python
* Pandas
* NumPy

### Database

* PostgreSQL
* SQLAlchemy
* psycopg2

### Machine Learning

* Scikit-Learn
* Random Forest Regressor

### Dashboard

* Streamlit
* Plotly

### Data Sources

* Spotify Web API
* Kaggle Dataset

### Utilities

* dotenv
* logging
* schedule

---

## Folder Structure

```text
spotify-etl-pipeline/
│
├── dashboard/
│   └── app.py
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── load_api.py
│   ├── spotify_api.py
│   ├── train_model.py
│   ├── model_comparison.py
│   ├── pipeline.py
│   └── db_config.py
│
├── models/
│
├── assets/
│
├── sql/
│
├── data/
│
├── requirements.txt
├── README.md
├── .env.example
└── main.py
```

---

## Machine Learning Pipeline

### Target Variable

```text
popularity
```

### Features Used

Original Features:

* danceability
* energy
* tempo
* valence
* loudness
* speechiness
* acousticness
* instrumentalness
* liveness
* duration

Additional Features:

* genre
* explicit
* key
* mode
* time_signature

Engineered Features:

* energy_danceability
* energy_valence
* tempo_energy

---

## Model Performance

### Random Forest Regressor

Performance:

```text
Train R² Score : 0.91
Test R² Score  : 0.48
MAE            : 9.98
```

### Model Comparison

| Model             | MAE   | R²   |
| ----------------- | ----- | ---- |
| Random Forest     | 9.98  | 0.48 |
| Gradient Boosting | 13.64 | 0.28 |
| Linear Regression | 16.33 | 0.04 |

Random Forest provided the best performance and was selected as the final model.

---

## Feature Importance

Most influential features identified by the model:

1. Acousticness
2. Loudness
3. Speechiness
4. Liveness
5. Danceability
6. Tempo
7. Valence
8. Energy-Danceability Interaction
9. Instrumentalness
10. Energy

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd spotify-etl-pipeline
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create:

```bash
cp .env.example .env
```

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=spotify_db
DB_USER=postgres
DB_PASSWORD=your_password

SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

---

## Running the Project

### Run ETL Pipeline

```bash
python main.py
```

### Train Model

```bash
python -m src.train_model
```

### Compare Models

```bash
python -m src.model_comparison
```

### Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Dashboard Modules

### API Analytics

Analyze live Spotify API data.

### Audio Feature Analytics

Explore:

* Danceability
* Energy
* Tempo
* Popularity
* Genre Trends

### Artist Analytics

View:

* Top Artists
* Average Popularity
* Track Distribution

### Popularity Predictor

Input song characteristics and estimate expected popularity score.

---

## Learning Outcomes

This project demonstrates:

* ETL Design
* Data Warehousing
* PostgreSQL Integration
* API Consumption
* Feature Engineering
* Supervised Machine Learning
* Model Evaluation
* Dashboard Development
* End-to-End Data Science Workflow

---

## Future Enhancements

* XGBoost Model
* Recommendation System
* Streamlit Cloud Deployment
* Airflow Orchestration
* Docker Containerization
* Real-Time Data Pipeline
* User Authentication
* Prediction History Tracking

---

## Author

Sujan A K

B.Tech Artificial Intelligence & Data Science

KCG College of Technology

```
```
