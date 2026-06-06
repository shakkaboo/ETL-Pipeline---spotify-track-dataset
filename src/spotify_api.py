import os
import base64
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"


def get_spotify_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Spotify API credentials are missing in .env file")

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(
        SPOTIFY_TOKEN_URL,
        headers=headers,
        data=data,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["access_token"]


def search_tracks(query="pop", limit=50):
    token = get_spotify_token()

    headers = {
        "Authorization": f"Bearer {token}",
    }

    params = {
        "q": query,
        "type": "track",
        "limit": limit,
        "market": "IN",
    }

    response = requests.get(
        SPOTIFY_SEARCH_URL,
        headers=headers,
        params=params,
        timeout=30,
    )

    if response.status_code != 200:
        print("Spotify search error:")
        print("Status code:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()
    tracks = response.json()["tracks"]["items"]

    track_data = []

    for track in tracks:
        artists = ", ".join([artist["name"] for artist in track["artists"]])

        track_data.append(
            {
                "track_id": track.get("id"),
                "track_name": track.get("name"),
                "artists": artists,
                "album_name": track.get("album", {}).get("name"),
                "release_date": track.get("album", {}).get("release_date"),
                "popularity": track.get("popularity"),
                "duration_ms": track.get("duration_ms"),
                "explicit": track.get("explicit"),
                "spotify_url": track.get("external_urls", {}).get("spotify"),
                "search_query": query,
            }
        )

    return pd.DataFrame(track_data)


def extract_tracks_from_api(queries=None, limit=50):
    if queries is None:
        queries = ["pop", "rock", "hip hop", "classical", "edm"]

    all_tracks = []

    for query in queries:
        print(f"Fetching tracks for query: {query}")
        df = search_tracks(query=query, limit=limit)
        all_tracks.append(df)

    final_df = pd.concat(all_tracks, ignore_index=True)
    final_df = final_df.drop_duplicates(subset=["track_id"])

    return final_df