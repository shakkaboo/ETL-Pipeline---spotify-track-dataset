import pandas as pd
from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
)

from src.db_config import get_db_url


engine = create_engine(get_db_url())

query = """
SELECT
    popularity,
    duration_ms,
    explicit,
    danceability,
    energy,
    key,
    loudness,
    mode,
    speechiness,
    acousticness,
    instrumentalness,
    liveness,
    valence,
    tempo,
    time_signature,
    track_genre,
    duration_min
FROM spotify_tracks_cleaned
"""

df = pd.read_sql(query, engine)

df = df.dropna()
df["energy_danceability"] = df["energy"] * df["danceability"]
df["energy_valence"] = df["energy"] * df["valence"]
df["tempo_energy"] = df["tempo"] * df["energy"]

numeric_features = [
    "duration_ms",
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "time_signature",
    "duration_min",
    "energy_danceability",
    "energy_valence",
    "tempo_energy",
]

categorical_features = [
    "explicit",
    "track_genre",
]

X = pd.get_dummies(
    df[numeric_features + categorical_features],
    columns=categorical_features,
    drop_first=True,
)

y = df["popularity"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        random_state=42,
    ),
}

results = []

for name, model in models.items():

    print(f"\nTraining {name}")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    r2 = r2_score(
        y_test,
        predictions,
    )

    results.append(
        {
            "Model": name,
            "MAE": round(mae, 2),
            "R2": round(r2, 3),
        }
    )

results_df = pd.DataFrame(results)

print("\nRESULTS")
print(results_df.sort_values(by="R2", ascending=False))