# 📑Design document

In this document we summarize how we plan to execute movieFinder project.

# 🔍Overview

# ⚡Motivation
Couples, friends and families constantly meet to watch a movie but can't decide which one. This engine could choose what movies would be optimal for you two to watch together.
# 🧮Success metrics
We will measure success for specific user as $S = \frac{\text{liked games}}{\text{total movies shown}}$


# 🚧Requirements & Constraints

## No user data at all

## No labeled data


# 🗝️Methodology

## Problem statement
As there is no test set, this task will not be specified as a standard supervised ML algorithm.
We have several options to explore
* Matrix factorization
* Online learning

## Learning alhorithm


## Data

We will use mainly to API's
* OMDb API
    * https://www.omdbapi.com/
* TMDB API
    * https://developer.themoviedb.org/docs/getting-started

# 👷Implementation
For now we plan to put Docker file on AWS EC2 containing
* python backend
* django/flask app

## Important architectural choices
Do we use sql database inside docker container or SQL database hosted on cloud.

## Phases
* Engine - Phase I
* Web app + Docker image - Phase II
* AWS - Phase III


## Deadlines
* 31.07.2024 - Deadline for Phase I
* 21.08.2024 - Deadline for Phase II
* 31.08.2024 - Deadline for Phase III
