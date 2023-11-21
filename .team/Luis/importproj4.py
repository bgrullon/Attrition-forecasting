import pandas as pd
import sqlite3

# Read the CSV file into a DataFrame
df = pd.read_csv('C:\\Users\\benny\\Github\\Attrition-forecasting\\data\\customer_churn.csv')

# Create a SQLite database and a connection to it
conn = sqlite3.connect('proj4data.sqlite')

# Write the DataFrame to a new table in the SQLite database
df.to_sql('mytable', conn, index=False)

# Close the database connection
conn.close()