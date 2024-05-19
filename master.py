import sys
sys.path.append("../APIKEYS")

import apiKey
ymdbapiURL = "https://www.omdbapi.com/?i=tt3896198&"
tmdbURL = "https://www.omdbapi.com/?i=tt3896198&"
tmdbDiscoverURL = "https://api.themoviedb.org/3/discover/movie"

import json
import requests


if __name__ == "__main__":
    header = {
        "apikey" : apiKey.OMDBAPIKEY
    }

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
        print("Success!")

        json_formatted_str = json.dumps(response.json(), indent=3)
        print(json_formatted_str)
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
