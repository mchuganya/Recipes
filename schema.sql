-- SQLite schema for recipes
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cuisine VARCHAR(255),
    title VARCHAR(1024) NOT NULL,
    rating FLOAT,
    prep_time INTEGER,
    cook_time INTEGER,
    total_time INTEGER,
    description TEXT,
    nutrients TEXT,
    serves VARCHAR(255),
    calories INTEGER
);
