DO $$  
BEGIN  
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'afisha_db') THEN  
        CREATE DATABASE afisha_db;  
    END IF;  
END $$; 
 
\c afisha_db 
 
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    location TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

