import pandas as pd
import sqlite3

# Read the CSV file into a DataFrame
df = pd.read_csv('C:\\Users\\kingl\\Downloads\\ipc-county\\data\\Project_Data.csv')

# Create a SQLite database and a connection to it
conn = sqlite3.connect('projdata3.sqlite')

# Write the DataFrame to a new table in the SQLite database
df.to_sql('mytable', conn, index=False)

# Close the database connection
conn.close()