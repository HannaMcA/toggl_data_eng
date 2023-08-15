# Toggl Data Engineering Home Assignment

This project involves an Extract, Transform, Load (ETL) process to retrieve job data related to data engineering positions, transform it, and load it into a PostgreSQL database. The project also includes Dockerization for easy deployment.

## Project Structure

The project directory contains the following files and folders:

- `etl_script.py`: Python script responsible for performing the ETL process.
- `requirements.txt`: List of Python dependencies required for the project.
- `Dockerfile`: Docker configuration to create a containerized environment.
- `sql_scripts`: Folder containing SQL scripts for creating database tables and views.
  - `create_chicago_de_jobs.sql`: SQL script to create a view for Chicago-based intermediate data engineering jobs.
  - `create_usa_de_jobs_location.sql`: SQL script to create the `usa_de_jobs_location` table.
  - `create_usa_de_jobs_offering_type.sql`: SQL script to create the `usa_de_jobs_offering_type` table.
  - `create_usa_de_jobs_renumeration.sql`: SQL script to create the `usa_de_jobs_renumeration` table.
  - `create_usa_de_jobs.sql`: SQL script to create the `usa_de_jobs` table.

## Usage

1. Make sure you have Docker installed on your system.

2. Clone this repository to your local machine.

3. Navigate to the project directory in your terminal.

4. Build the Docker image using the following command:
   ```bash
   docker build -t data-engineering-etl .
   docker run --rm -it data-engineering-etl

## Data Model
The DDLs for each table can be located in the sql_scripts directory. `usa_de_jobs` has a one to many relationship with `usa_de_jobs_location`, `usa_de_jobs_renumeration`, and `usa_de_jobs_offering_type`.

## Database
 This application persists data to the host of a GCP Postgres database.
