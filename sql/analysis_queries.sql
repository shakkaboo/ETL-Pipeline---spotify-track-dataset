-- ============================================
-- Spotify Tracks Analysis Queries
-- ============================================

-- 1. Top 10 most popular tracks
SELECT track_name, artists, popularity
FROM spotify_tracks_cleaned
ORDER BY popularity DESC
LIMIT 10;

-- 2. Most popular artists (by average popularity)
SELECT artists,
       ROUND(AVG(popularity), 2) AS avg_popularity,
       COUNT(*) AS track_count
FROM spotify_tracks_cleaned
GROUP BY artists
ORDER BY avg_popularity DESC
LIMIT 10;

-- 3. Average popularity by genre
SELECT track_genre,
       ROUND(AVG(popularity), 2) AS avg_popularity,
       COUNT(*) AS track_count
FROM spotify_tracks_cleaned
GROUP BY track_genre
ORDER BY avg_popularity DESC;

-- 4. Average danceability by genre
SELECT track_genre,
       ROUND(AVG(danceability), 3) AS avg_danceability,
       COUNT(*) AS track_count
FROM spotify_tracks_cleaned
GROUP BY track_genre
ORDER BY avg_danceability DESC;

-- 5. Average energy by genre
SELECT track_genre,
       ROUND(AVG(energy), 3) AS avg_energy,
       COUNT(*) AS track_count
FROM spotify_tracks_cleaned
GROUP BY track_genre
ORDER BY avg_energy DESC;

-- 6. Most danceable tracks
SELECT track_name, artists, danceability, energy, valence
FROM spotify_tracks_cleaned
ORDER BY danceability DESC
LIMIT 10;

-- 7. High-energy workout songs (energy >= 0.8)
SELECT track_name, artists, energy, tempo, danceability
FROM spotify_tracks_cleaned
WHERE energy >= 0.8
ORDER BY energy DESC
LIMIT 20;

-- 8. Happy / energetic songs (mood_category = 'Happy/Energetic')
SELECT track_name, artists, valence, energy, danceability
FROM spotify_tracks_cleaned
WHERE mood_category = 'Happy/Energetic'
ORDER BY valence DESC
LIMIT 20;

-- 9. Calm songs (mood_category = 'Calm')
SELECT track_name, artists, valence, energy, acousticness
FROM spotify_tracks_cleaned
WHERE mood_category = 'Calm'
ORDER BY acousticness DESC
LIMIT 20;

-- 10. Songs grouped by mood category
SELECT mood_category,
       COUNT(*) AS song_count,
       ROUND(AVG(popularity), 2) AS avg_popularity,
       ROUND(AVG(duration_min), 2) AS avg_duration_min
FROM spotify_tracks_cleaned
GROUP BY mood_category
ORDER BY song_count DESC;

-- 11. Genre-wise average tempo
SELECT track_genre,
       ROUND(AVG(tempo), 2) AS avg_tempo,
       MIN(tempo) AS min_tempo,
       MAX(tempo) AS max_tempo,
       COUNT(*) AS track_count
FROM spotify_tracks_cleaned
GROUP BY track_genre
ORDER BY avg_tempo DESC;

-- 12. ML-Ready Dataset Query (numerical features only)
SELECT
    popularity,
    duration_ms,
    danceability,
    energy,
    loudness,
    speechiness,
    acousticness,
    instrumentalness,
    liveness,
    valence,
    tempo,
    duration_min
FROM spotify_tracks_cleaned
WHERE popularity IS NOT NULL
  AND danceability IS NOT NULL
  AND energy IS NOT NULL;
