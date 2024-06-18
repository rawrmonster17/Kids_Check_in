-- Create kids table if it does not exist
CREATE TABLE IF NOT EXISTS kids (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    allergies TEXT,
    checked_in BOOLEAN NOT NULL
);

-- Create parents table if it does not exist
CREATE TABLE IF NOT EXISTS parents (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100) NOT NULL
);

-- Create parent_kid table if it does not exist
CREATE TABLE IF NOT EXISTS parent_kid (
    parent_id INT NOT NULL,
    kid_id INT NOT NULL,
    PRIMARY KEY (parent_id, kid_id),
    FOREIGN KEY (parent_id) REFERENCES parents(id) ON DELETE CASCADE,
    FOREIGN KEY (kid_id) REFERENCES kids(id) ON DELETE CASCADE
);

-- Create users table if it does not exist
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL
);
