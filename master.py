import sys
sys.path.append("../APIKEYS")

import apiKey
from src.API import tmdb

headers = {
        "accept": "application/json",
        "Authorization": apiKey.TMDBBEARER
    }

if __name__ == "__main__":

    #tmdb_discover = pd.read_parquet("tmdb_discover.parquet")
    #tmdb_discover.to_parquet("tmdb_discover.parquet")
    TL = tmdb.throttleLimiter(1, _headers=headers, verbose=True)
    result = TL.multipleDiscoverRequests(10, 1, 800, 0.5)
    print(result)
