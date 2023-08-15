CREATE OR REPLACE VIEW chicago_de_jobs AS
    SELECT 
        jobs.JobID, 
        jobs.PositionID, 
        jobs.PositionTitle, 
        jobs.PositionURI, 
        jobs.PositionStartDate, 
        jobs.PositionEndDate, 
        jobs.PublicationStartDate, 
        jobs.ApplicationCloseDate,
        location.LocationName, 
        location.CityName,
        renumeration.MinimumRange, 
        renumeration.MaximumRange, 
        renumeration.RateIntervalCode, 
        renumeration.Description,
        ot.OfferingName, 
        ot.OfferingCode,
        jobs.PositionLowGrade,
        jobs.PositionHighGrade
    FROM usa_de_jobs jobs
    LEFT JOIN usa_de_jobs_location location ON jobs.JobID = location.JobID
    LEFT JOIN usa_de_jobs_renumeration renumeration ON jobs.JobID = renumeration.JobID
    LEFT JOIN usa_de_jobs_offering_type ot ON jobs.JobID = ot.JobID 
    WHERE
        lower(location.LocationName) = 'chicago, illinois'
        AND jobs.PositionLowGrade >= 5
        AND jobs.PositionHighGrade <= 10   