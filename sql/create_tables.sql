-- Create the spotify_tracks_cleaned table
CREATE TABLE IF NOT EXISTS spotify_tracks_cleaned (
    id SERIAL PRIMARY KEY,
    track_id VARCHAR(255) UNIQUE,
    artists TEXT,
    album_name TEXT,
    track_name TEXT,
    popularity INTEGER,
    duration_ms BIGINT,
    explicit BOOLEAN,
    danceability FLOAT,
    energy FLOAT,
    key INTEGER,
    loudness FLOAT,
    mode INTEGER,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    time_signature INTEGER,
    track_genre VARCHAR(255),
    duration_min FLOAT,
    popularity_category VARCHAR(20),
    energy_level VARCHAR(20),
    danceability_level VARCHAR(20),
    mood_category VARCHAR(50)
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_track_genre ON spotify_tracks_cleaned (track_genre);
CREATE INDEX IF NOT EXISTS idx_popularity ON spotify_tracks_cleaned (popularity);
CREATE INDEX IF NOT EXISTS idx_mood_category ON spotify_tracks_cleaned (mood_category);
