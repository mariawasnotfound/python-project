CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT,
    date TIMESTAMP,
    available_seats BOOLEAN,
    contact_info TEXT
);
