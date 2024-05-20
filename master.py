import sys
sys.path.append("../APIKEYS")

import apiKey

import json
import requests
import pandas as pd
from datetime import datetime
import warnings


def getPopularMovies(language : str, page : int):
    """
    Uses tbdb database to get popular movies.
    It's a subset of discover endpoint

    Args:
    language
        original language of movie, e.g. 'en-US'
    page
        what page API have to return
    """

    tmdbPopularURL = "https://api.themoviedb.org/3/movie/popular"

    headers = {
        "accept": "application/json",
        "Authorization": apiKey.TMDBBEARER
    }

    params = {
        "language": language,
        "page": str(page)
    }

    response = requests.get(tmdbPopularURL, headers=headers, params=params)

    result_df = pd.DataFrame(response.json()['results'])
    result_df['downloadDatetime'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    result_df['page'] = response.json()['page']
    return result_df

def discover():
    """
    Uses tbdb database for discovering new titles


    """
    warnings.warn("This function is not yet implemented. Use getPopularMovies() for now")
    tmdbDiscoverURL = "https://api.themoviedb.org/3/discover/movie"

    headers = {
        "accept": "application/json",
        "Authorization": apiKey.TMDBBEARER
    }

    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": "1",
        "sort_by": "vote_average.desc, vote_count.desc"
    }

    response = requests.get(tmdbDiscoverURL, headers=headers, params=params)

    if response.status_code == 200:
        json_formatted_str = json.dumps(response.json(), indent=3)
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)

    result_df = pd.DataFrame(response.json())
    result_df['downloadDatetime'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    result_df['page'] = response.json()['page']
    return result_df

if __name__ == "__main__":
    tmdb_database = pd.read_parquet("tmdb_database.parquet")
    tmdb_latest_page = tmdb_database['page'].max()
    
    tmdb_database = pd.concat([tmdb_database, getPopularMovies("en-US", tmdb_latest_page + 1)],
                              axis="rows")
    tmdb_database.to_parquet("tmdb_database.parquet")
