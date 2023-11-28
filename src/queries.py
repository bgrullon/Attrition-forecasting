# Dependencies
from dotenv import dotenv_values
import psycopg2
import csv

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


def Query_Data():
    # Create a connection using psycopg2
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Query the Redshift table
    query = f"""
    SELECT *
    FROM customers;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    return results