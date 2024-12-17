CREATE TABLE IF NOT EXISTS events ( 
    id SERIAL PRIMARY KEY, 
    title TEXT NOT NULL, 
    location TEXT, 
    latitude DOUBLE PRECISION, 
    longitude DOUBLE PRECISION, 
    start_time TIMESTAMP NOT NULL, 
    availability_status TEXT, 
    link TEXT 
);
