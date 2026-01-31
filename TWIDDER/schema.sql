CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT UNIQUE NOT NULL, 
    password TEXT NOT NULL,
    firstname TEXT,
    lastname TEXT,
    gender TEXT,
    city TEXT,
    country TEXT,
    messages TEXT,
    token TEXT
);