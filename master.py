import sys
sys.path.append("../APIKEYS")

import apiKey

import json
import time
import requests
import pandas as pd
from datetime import datetime
import warnings

headers = {
        "accept": "application/json",
        "Authorization": apiKey.TMDBBEARER
    }

def processRequest(url, headers, params) -> pd.DataFrame:
    """
    Get response and convert it to pandas.DataFrame with error handling.
    """
    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
        exit(0)

    result_df = pd.DataFrame(response.json()['results'])
    result_df['downloadDatetime'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    result_df['page'] = response.json()['page']
    return result_df

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

    params = {
        "language": language,
        "page": str(page)
    }
    return processRequest(tmdbPopularURL, headers, params)

def getTrendingMovies():
    """
    Gets trending movies this week from TMDB.
    """
    url = "https://api.themoviedb.org/3/trending/movie/week?language=en-US"

    params = {
        "time_window" : "week",
        "language" : "en-US"
    }

    return processRequest(url, headers=headers, params=params)

def discover(minimum_votes : int,
                  minimum_rating : int,
                  later_than : str,
                  earlier_than : str,
                  page : int) -> pd.DataFrame:
    """
    Uses tbdb database for discovering new movies.
    """
    tmdbDiscoverURL = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": page,
        "sort_by": "vote_average.desc, vote_count.desc",
        "release_date.lte" : earlier_than,
        "release_date.gte" : later_than,
        "vote_count.gte" : minimum_votes,
        "vote_average.gte" : minimum_rating
    }

    return processRequest(url=tmdbDiscoverURL, headers=headers, params=params)

class throttleLimiter():
    """
    This class provides an object useful for making API requests with 
    maximum number of requests per second.
    """

    def __init__(self, url : str, max_requests_per_sec : int):
        self.url = url
        self.sliding_window = [datetime.now() for i in range(max_requests_per_sec)]

    def makeRequest(self, params : dict, headers : dict = None):
        """
        This function checks whether max throttle is reached and than makes a request
        (or waits with request so that the throttle is not exceeded).

        Args
        params
            body of request in requests.get() function
        headers
            header of request in requests.get() function
        """
        
        time_diff = (datetime.now() - self.sliding_window[-1])

        if time_diff.seconds == 0:
            time_to_wait = 1- time_diff.microseconds/100000
            print(f"Throttle limit reached. Waiting {time_to_wait} seconds for resuming.")
            time.sleep(time_to_wait)

        #updating sliding window
        self.sliding_window.insert(0, datetime.now())
        self.sliding_window.pop()

        return processRequest(url=self.url, headers=headers, params=params)


if __name__ == "__main__":

    #discover(minimum_votes= 300,
    #                            minimum_rating=4.0,
    #                            later_than="1950-01-01",
    #                            earlier_than="2024-02-01", page=1).to_parquet("tmdb_discover.parquet")
    #
    #exit(0)
    tmdb_discover = pd.read_parquet("tmdb_discover.parquet")
    
    #getTrendingMovies().to_parquet("tmdb_trending.parquet")
    for i in range(30*100):
        print(f"---------------PROCESSING {i} PAGE---------------")
        if tmdb_discover.shape[0] < 5:
            tmdb_latest_page = 1
        else:
            tmdb_latest_page = tmdb_discover['page'].max() + 1
        
        tmdb_discover_new = discover(minimum_votes= 300,
                                minimum_rating=4.0,
                                later_than="1950-01-01",
                                earlier_than="2024-02-01",
                                page=tmdb_latest_page)
        tmdb_discover = pd.concat([tmdb_discover, tmdb_discover_new])
        time.sleep(0.03)
        tmdb_latest_page = tmdb_latest_page + 1
        
    tmdb_discover.to_parquet("tmdb_discover.parquet")
