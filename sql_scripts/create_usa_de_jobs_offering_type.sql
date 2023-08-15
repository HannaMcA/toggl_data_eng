CREATE TABLE IF NOT EXISTS usa_de_jobs_offering_type (
    OfferingID SERIAL PRIMARY KEY, 
    JobID INTEGER REFERENCES usa_de_jobs(JobID), 
    OfferingName TEXT, 
    OfferingCode INTEGER, 
    DateCreated TIMESTAMP
);