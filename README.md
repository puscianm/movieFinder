# Movie finder

# Project structure

**Back**
We plan to have python scripts with SQL database packed into docker and hosted on AWS.

**Front**
We plan to create simple website using flask or django

# Engine

We can seperate project maturity on two phases

## Initial phase

In this phase we plan to use unsupervised learning algorithm combined with reinforcement learning.
Cause of this approach is simple - we don't have labels inputed from users.

## End phase

In this phase we plan to use supervised learning algorithms for improvement in performance. 

# Main questions
How does one's previous liked movies correspond to movies that one would want to see. Do they want to see similar movie or a different one? Isn't user stuck in local max of their enjoyment of their movie? Maybe some this user would enjoy more watching movie from category which he's never seen. How do we encorporate data that we get from user. Do we take it into account in each iteration? Do we use online learning?

# Used APIs

In this project we use two main apis
* OMDb API
    * https://www.omdbapi.com/
* TMDB API
    * https://developer.themoviedb.org/docs/getting-started
