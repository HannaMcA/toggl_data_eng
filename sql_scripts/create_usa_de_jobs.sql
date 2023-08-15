CREATE TABLE IF NOT EXISTS usa_de_jobs (
    JobID SERIAL PRIMARY KEY, 
    PositionID TEXT, 
    PositionTitle TEXT, 
    PositionURI TEXT, 
    PositionLowGrade INTEGER, 
    PositionHighGrade INTEGER, 
    PositionStartDate TIMESTAMP, 
    PositionEndDate TIMESTAMP, 
    PublicationStartDate TIMESTAMP, 
    ApplicationCloseDate TIMESTAMP, 
    DateCreated TIMESTAMP
);