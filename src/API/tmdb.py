import json
import time
import requests
import pandas as pd
from datetime import datetime
import warnings

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
                  page : int,
                  headers) -> pd.DataFrame:
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

    def __init__(self, max_requests_per_sec : int, _headers : dict, verbose : bool = False):
        self.sliding_window = [datetime.now() for i in range(max_requests_per_sec - 1)]
        self.headers = _headers

    def makeRequest(self, params : dict, url : str):
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
            if self.verbose:
                print(f"Throttle limit reached. Waiting {time_to_wait} seconds for resuming.")
            time.sleep(time_to_wait)

        #updating sliding window
        self.sliding_window.insert(0, datetime.now())
        self.sliding_window.pop()

        return processRequest(url=url, headers=self.headers, params=params)
    
    def multipleDiscoverRequests(self, numberOfRequests : int, page_start : int, minimum_votes : int, minimum_rating : int):
        """
        Makes multiple requests to discover endpoint.

        Args
        numberOfRequests

        page_start

        minimum_votes

        minimum_rating
        """

        tmdbDiscoverURL = "https://api.themoviedb.org/3/discover/movie"

        tmdb_latest_page = page_start

        for i in range(numberOfRequests):
            print(f"---------------PROCESSING {i} PAGE---------------")
            tmdb_discover_new = discover(minimum_votes= minimum_votes,
                                    minimum_rating=minimum_rating,
                                    later_than="1950-01-01",
                                    earlier_than="2024-02-01",
                                    page=tmdb_latest_page,
                                    headers=self.headers)
            
            try:
                tmdb_discover = pd.concat([tmdb_discover, tmdb_discover_new])
            except UnboundLocalError:
                tmdb_discover = tmdb_discover_new

            tmdb_latest_page = tmdb_latest_page + 1
        
        return tmdb_discover
