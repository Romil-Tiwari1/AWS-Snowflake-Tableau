import yfinance as yf
import json
import boto3
from io import StringIO

# Initialize the S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Define the stock symbol and S3 bucket details
    stock_symbol = event.get('stock_symbol', 'TSLA')  # Default to TSLA if not provided
    bucket_name = 'aws-snowflake-project'  # Replace with your S3 bucket name
    file_name = f"{stock_symbol}_data.csv"
    s3_path = f"stock_data/{file_name}"

    # Fetch stock data
    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period="1mo")  # Fetch 1 month of historical data

    # Convert DataFrame to CSV
    csv_buffer = StringIO()
    hist.to_csv(csv_buffer)

    # Upload the CSV to S3
    s3.put_object(Bucket=bucket_name, Key=s3_path, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully uploaded {file_name} to {s3_path}')
    }
