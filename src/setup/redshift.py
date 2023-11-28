# Dependencies
from dotenv import dotenv_values
import psycopg2
import csv
from pathlib import Path

dbpass = dotenv_values().get('dbpassword')
access = dotenv_values().get('aws_access_key_id')
secret = dotenv_values().get('aws_secret_access_key')
iam_role = dotenv_values().get('redshift_iam_role')
s3_bucket = 'redshift-bucket-project-4'


# Replace these values with your actual Redshift credentials
redshift_credentials = {
    'host': 'tf-redshift-cluster.cvywpgklj7zv.us-east-1.redshift.amazonaws.com',
    'port': 5439,
    'database': 'mydb',
    'user': 'admin',
    'password': dbpass
}

# Create a connection string
connection_string = f"dbname={redshift_credentials['database']} user={redshift_credentials['user']} password={redshift_credentials['password']} host={redshift_credentials['host']} port={redshift_credentials['port']}"

# function to create the Redshift table
def CreateRedshiftTable():
    # Create a connection using psycopg2
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Create the table
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS customers (
        customer_ID VARCHAR PRIMARY KEY,
        gender VARCHAR,
        senior_citizen INTEGER,
        partner VARCHAR,
        dependants VARCHAR,
        tenure INTEGER,
        phone_service VARCHAR,
        multiple_lines VARCHAR,
        internet_service VARCHAR,
        online_security VARCHAR,
        online_backup VARCHAR,
        device_protection VARCHAR,
        tech_support VARCHAR,
        streaming_TV VARCHAR,
        streaming_movies VARCHAR,
        contract VARCHAR,
        paperless_billing VARCHAR,
        payment_method VARCHAR,
        monthly_charges FLOAT,
        total_charges FLOAT,
        churn VARCHAR
    );
    """

    cursor.execute(create_table_query)
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

# function to insert the CSV data into the Redshift table
def InsertIntoRedshift():
    # Create a connection using psycopg2
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Copy the CSV file from S3 to the Redshift table
    copy_query = f"""
    COPY customers
    FROM 's3://{s3_bucket}/customer_churn.csv'
    IAM_ROLE '{iam_role}'
    DELIMITER ',' 
    IGNOREHEADER 1
    CSV;
    """

    cursor.execute(copy_query)
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()
