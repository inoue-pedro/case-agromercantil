import boto3
import pandas as pd
import io

# Initialize the S3 client
s3 = boto3.client('s3')

bucket_name = 'your-bucket-name'
file_key = 'path/to/your/file.parquet'

# Read the Parquet file from S3
try:
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    
    # Read the Parquet file into a pandas DataFrame
    file_content = response['Body'].read()
    df = pd.read_parquet(io.BytesIO(file_content))

    # Transformation. Creating new column by calculating average from column 'A'
    df['A_avg'] = df['A'].mean() 
    
    print(df.head())
    
except Exception as e:
    print(f"Error reading Parquet file from S3: {e}")
