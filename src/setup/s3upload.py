# Dependencies
from dotenv import dotenv_values
import boto3
from pathlib import Path

dbpass = dotenv_values().get('dbpassword')
access = dotenv_values().get('aws_access_key_id')
secret = dotenv_values().get('aws_secret_access_key')

# Upload the CSV file to S3
s3_bucket_name = 'redshift-bucket-project-4'
s3_object_name = Path('data/customer_churn.csv')  

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)

# Upload the file
s3.upload_file(str(s3_object_name), s3_bucket_name, "customer_churn.csv")

print(f"File '{s3_object_name}' uploaded to '{s3_bucket_name}'")