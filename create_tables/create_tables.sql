CREATE TABLE IF NOT EXISTS schedule (
    match_begin_time TIME,
    host_name VARCHAR(255),
    guest_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS tmdb_database (
    adult BOOLEAN,
    backdrop_path VARCHAR(255),
    genre_ids VARCHAR(255),
    id INTEGER,
    original_language VARCHAR(255),
    original_title VARCHAR(255),
    overview VARCHAR(255),
    popularity DECIMAL,
    poster_path VARCHAR(255),
    release_date DATE,
    title VARCHAR(255),
    video BOOLEAN,
    vote_average DECIMAL,
    vote_count INTEGER,
    downloadDatetime TIME WITHOUT TIME ZONE,
    page INTEGER
);
