CREATE TABLE IF NOT EXISTS usa_de_jobs_location (
    locationID SERIAL PRIMARY KEY, 
    JobID INTEGER REFERENCES usa_de_jobs(JobID), 
    LocationName TEXT, 
    CityName TEXT, 
    DateCreated TIMESTAMP
);