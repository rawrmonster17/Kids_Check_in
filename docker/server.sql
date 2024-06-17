-- Create the database
CREATE DATABASE IF NOT EXISTS kids;

-- Use the kids database
\c kids;

-- Create tables
CREATE TABLE IF NOT EXISTS kids (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    allergies TEXT,
    checked_in BOOLEAN
);

CREATE TABLE IF NOT EXISTS parents (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone_number VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS parent_kid (
    parent_id INTEGER REFERENCES parents(id),
    kid_id INTEGER REFERENCES kids(id),
    PRIMARY KEY (parent_id, kid_id)
);
