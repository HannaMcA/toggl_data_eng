import requests
import psycopg2
from datetime import datetime

# API key
api_key = "gh3jLR00nD4jPbv2Z4GUEwkWfGtyQvz96Kc3JeHTDa0="

# Base API URL
base_url = "https://data.usajobs.gov/api/search"

# Search criteria
search_params = {
    "Keyword": "data engineering",
}

sql_create_table_script_names = [
    "create_usa_de_jobs.sql",
    "create_usa_de_jobs_renumeration.sql",
    "create_usa_de_jobs_location.sql",
    "create_usa_de_jobs_offering_type.sql"
]
# Database connection parameters
host = "34.171.51.65"
database = "postgres"
user = "postgres"
password = "toggl2023"

try:
    # Establish a connection to the PostgreSQL database
    pgdb_conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    # Create a cursor object to interact with the database
    pgdb_cursor = pgdb_conn.cursor()

    # Iterate through SQL script files and create tables
    for filename in sql_create_table_script_names:
        with open(f"sql_scripts/{filename}", "r") as sql_file:
            sql_query = sql_file.read()
            pgdb_cursor.execute(sql_query)
            pgdb_conn.commit()
        print(f"{filename} executed successfully!")

except (Exception, psycopg2.Error) as error:
    print("Error connecting to the database:", error)

# API request function
def make_api_request(url, params):
    headers = {"Host": "data.usajobs.gov", "User-Agent": "ETL Script", "Authorization-Key": api_key}
    response = requests.get(url, params=params, headers=headers)
    return response.json()

# Perform the ETL process
def perform_etl():
    try:
        response = make_api_request(base_url, search_params)
        
        if "SearchResult" in response:
            jobs = response["SearchResult"]["SearchResultItems"]
            
            for job in jobs:
                #Insert into usa_de_jobs table
                position_id = job["MatchedObjectDescriptor"]["PositionID"]
                position_title = job["MatchedObjectDescriptor"]["PositionTitle"]
                position_uri = job["MatchedObjectDescriptor"]["PositionURI"]
                position_low_grade = job["MatchedObjectDescriptor"]["UserArea"]["Details"]["LowGrade"]
                position_high_grade = job["MatchedObjectDescriptor"]["UserArea"]["Details"]["HighGrade"]
                position_st_dt = job["MatchedObjectDescriptor"]["PositionStartDate"]
                position_end_dt = job["MatchedObjectDescriptor"]["PositionEndDate"]
                publication_st_dt = job["MatchedObjectDescriptor"]["PublicationStartDate"]
                app_end_dt = job["MatchedObjectDescriptor"]["ApplicationCloseDate"]

                #determine if record exists in database
                pgdb_cursor.execute("SELECT PositionID FROM usa_de_jobs WHERE PositionID = %s;", (position_id,))
                existing_record = pgdb_cursor.fetchone()

                if not existing_record:

                    # SQL query with parameters
                    insert_query = "INSERT INTO usa_de_jobs (PositionID, PositionTitle, PositionURI, PositionLowGrade, PositionHighGrade, PositionStartDate, PositionEndDate, PublicationStartDate, ApplicationCloseDate, DateCreated) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                            RETURNING JobID;"

                    # Execute the query with the provided data
                    pgdb_cursor.execute(insert_query, (position_id, position_title, position_uri, position_low_grade, position_high_grade, position_st_dt, position_end_dt, publication_st_dt, app_end_dt, datetime.now()))          

                    parent_id = pgdb_cursor.fetchone()[0]


                    #Insert into usa_de_jobs_renumeration table
                    position_remuneration = job["MatchedObjectDescriptor"]["PositionRemuneration"]
                    for entry in position_remuneration:
                        minimum_range = float(entry["MinimumRange"])
                        maximum_range = float(entry["MaximumRange"])
                        rate_interval_code = entry["RateIntervalCode"]
                        description = entry["Description"]

                        insert_query = "INSERT INTO usa_de_jobs_renumeration (JobID, MinimumRange, MaximumRange, RateIntervalCode, Description, DateCreated) \
                        VALUES (%s, %s, %s, %s, %s, %s);"

                        pgdb_cursor.execute(insert_query, (parent_id, minimum_range, maximum_range, rate_interval_code, description, datetime.now()))          

                    #Insert into usa_de_jobs_location table
                    position_location = job["MatchedObjectDescriptor"]["PositionLocation"]
                    for entry in position_location:
                        location_name = entry["LocationName"]
                        city_name = entry["CityName"]

                        insert_query = "INSERT INTO usa_de_jobs_location (JobID, LocationName, CityName, DateCreated) \
                        VALUES (%s, %s, %s, %s);"

                        pgdb_cursor.execute(insert_query, (parent_id, location_name, city_name, datetime.now()))          

                    #Insert into usa_de_jobs_offering_type table
                    position_offering_type = job["MatchedObjectDescriptor"]["PositionOfferingType"]
                    for entry in position_offering_type:
                        offering_name = entry["Name"]
                        offering_code = int(entry["Code"])

                        insert_query = "INSERT INTO usa_de_jobs_offering_type (JobID, OfferingName, OfferingCode, DateCreated) \
                        VALUES (%s, %s, %s, %s);"

                        pgdb_cursor.execute(insert_query, (parent_id, offering_name, offering_code, datetime.now()))          
                else:
                    print("record exists")
            pgdb_conn.commit()
            print("ETL process completed successfully.")
            
        else:
            print("No search results found.")
    except Exception as e:
        print("An error occurred:", e)

def create_update_view():
    try:
        # Create the view
        with open("sql_scripts/create_chicago_de_jobs.sql", "r") as sql_file:
            create_view_query = sql_file.read()
            pgdb_cursor.execute(create_view_query)
            pgdb_conn.commit()

        print("View created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

# Main function
if __name__ == "__main__":
    perform_etl()
    create_update_view()
    
    # Close the cursor and connection
    if pgdb_cursor:
        pgdb_cursor.close()
    if pgdb_conn:
        pgdb_conn.close()

