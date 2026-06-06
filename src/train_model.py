import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from src.db_config import get_db_url


def train_popularity_model():
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

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    train_predictions = model.predict(X_train)

    train_r2 = r2_score(y_train, train_predictions)
    test_r2 = r2_score(y_test, predictions)

    print(f"Train R2 Score: {train_r2:.2f}")
    print(f"Test R2 Score: {test_r2:.2f}")

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("Model training completed")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R2 Score: {r2:.2f}")

    importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False
    )

    print("\nTop 15 Important Features:")
    print(importance_df.head(15))


    joblib.dump(model, "models/popularity_model.pkl")
    joblib.dump(
        X.columns.tolist(),
        "models/model_features.pkl"
    )

    print("Model saved to models/popularity_model.pkl")


if __name__ == "__main__":
    train_popularity_model()