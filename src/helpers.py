# Dependencies
from dotenv import dotenv_values
import psycopg2
import csv
import random
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import tensorflow as tf
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


def generate_fake_data(n):
    fake_data = []
    tenure = 1
    monthly_charges = random.randint(60, 118)
    gen_data = {
        "gender": ["Female", "Male"],
        "senior_citizen": ["Yes", "No"],
        "partner": ["Yes", "No"],
        "dependants": ["Yes", "No"],
        "tenure": 1,
        "phone_service": ["Yes", "No"],
        "multiple_lines": ["Yes", "No", "No phone service"],
        "internet_service": ["DSL", "Fiber optic", "No"],
        "online_security": ["Yes", "No", "No internet service"],
        "online_backup": ["Yes", "No", "No internet service"],
        "device_protection": ["Yes", "No", "No internet service"],
        "tech_support": ["Yes", "No", "No internet service"],
        "streaming_TV": ["Yes", "No", "No internet service"],
        "streaming_movies": ["Yes", "No", "No internet service"],
        "contract": ["Month-to-month", "One year", "Two year"],
        "paperless_billing": ["Yes", "No"],
        "payment_method": ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
        "monthly_charges": monthly_charges,
        "total_charges": monthly_charges * tenure,
    }

    # loop through n times and randomly generate data by selecting from gen_data
    for _ in range(n):
        customer = {}
        for key, value in gen_data.items():
            if isinstance(value, list):
                customer[key] = random.choice(value)
            else:
                customer[key] = value
        fake_data.append(customer)

    return fake_data

# function to predict attrition off generated data
def get_predictions(data):
    # convert data to dataframe
    attrition_df = pd.DataFrame(data)
    result_df = pd.DataFrame(data)

    # Initialize LabelEncoder
    label_encoder = LabelEncoder()

    # Apply LabelEncoder to the 'gender' column
    attrition_df['gender'] = label_encoder.fit_transform(attrition_df['gender'])
    attrition_df['total_charges'] = pd.to_numeric(attrition_df['total_charges'], errors='coerce')
    attrition_df['total_charges'].fillna(attrition_df['total_charges'].mean(), inplace=True)
    attrition_df['service_count'] = attrition_df[['phone_service', 'multiple_lines', 'internet_service', 'online_security', 'online_backup', 'device_protection', 'tech_support', 'streaming_TV', 'streaming_movies']].apply(lambda x: x.str.contains('Yes').sum(), axis=1)
    attrition_df = pd.get_dummies(attrition_df)
    # apply standard scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(attrition_df)
    # load model and predict
    model = tf.keras.models.load_model(Path('src', 'customer_churn.h5'))
    predictions = model.predict(X_scaled)
    # convert predictions to 1 or 0
    predictions = [1 if x > 0.5 else 0 for x in predictions]
    # convert predictions to "Yes" or "No"
    predictions = ['Yes' if x == 1 else 'No' for x in predictions]
    # combine predictions with data
    result_df['churn'] = predictions
    # turn into list of dictionaries
    predictions = result_df.to_dict('records')

    return predictions
