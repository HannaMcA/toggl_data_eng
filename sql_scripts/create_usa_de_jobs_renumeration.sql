CREATE TABLE IF NOT EXISTS usa_de_jobs_renumeration (
    RenumerationID SERIAL PRIMARY KEY, 
    JobID INTEGER REFERENCES usa_de_jobs(JobID), 
    MinimumRange FLOAT, 
    MaximumRange FLOAT, 
    RateIntervalCode TEXT, 
    Description TEXT, 
    DateCreated TIMESTAMP
);