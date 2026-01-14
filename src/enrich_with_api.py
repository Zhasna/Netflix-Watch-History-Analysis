import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

df = pd.read_csv("data/processed/cleaned_viewing.csv")

unique_titles = df["title"].dropna().unique()

def fetch_omdb_metadata(title):
    """
    Fetch genre, year, and type for a title from OMDb
    """
    url = "http://www.omdbapi.com/"
    params = {
        "apikey": OMDB_API_KEY,
        "t": title
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return "Unknown", None, None

    data = response.json()

    if data.get("Response") == "False":
        return "Unknown", None, None

    genre = data.get("Genre", "Unknown")
    year = data.get("Year")
    media_type = data.get("Type")

    return genre, year, media_type

metadata_rows = []

for title in unique_titles:
    genre, year, media_type = fetch_omdb_metadata(title)
    metadata_rows.append({
        "title": title,
        "genre": genre,
        "year": year,
        "media_type": media_type
    })

metadata_df = pd.DataFrame(metadata_rows)

metadata_df.to_csv("data/processed/title_metadata.csv", index=False)

enriched_df = df.merge(metadata_df, on="title", how="left")

enriched_df.to_csv("data/processed/enriched_viewing.csv", index=False)

print("OMDb enrichment completed successfully.")

