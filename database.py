# Dependencies
from dotenv import dotenv_values
import psycopg2
import csv

dbpass = dotenv_values().get('dbpassword')
access = dotenv_values().get('aws_access_key_id')
secret = dotenv_values().get('aws_secret_access_key')


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

# Try to establish a connection
csv_file_path = 'C:\\Users\\benny\\Github\\Attrition-forecasting\\data\\dataset.csv'
redshift_table = 'tf-redshift-cluster'

# Create a connection using psycopg2
conn = psycopg2.connect(connection_string)

# Create a cursor
cursor = conn.cursor()

# Query a single row from the Redshift table
query_row_command = f"SELECT * FROM {redshift_table}"
cursor.execute(query_row_command)
queried_customer = cursor.fetchone()

# Print the queried customer's information
if queried_customer:
    print(f"Queried Customer: {queried_customer}")
else:
    print("Customer not found.")

# Close the cursor and connection
cursor.close()
conn.close()