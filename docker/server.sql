-- Drop old tables if they exist
DROP TABLE IF EXISTS parent_kid;
DROP TABLE IF EXISTS kids;
DROP TABLE IF EXISTS parents;

-- Create users table if it does not exist
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL
);

-- Create families table if it does not exist
CREATE TABLE IF NOT EXISTS families (
    id SERIAL PRIMARY KEY,
    parent_first_name VARCHAR(50) NOT NULL,
    parent_last_name VARCHAR(50) NOT NULL,
    parent_phone_number VARCHAR(20),
    parent_email VARCHAR(100) NOT NULL,
    kid_first_name VARCHAR(50) NOT NULL,
    kid_last_name VARCHAR(50) NOT NULL,
    kid_allergies TEXT,
    kid_checked_in BOOLEAN NOT NULL
);
