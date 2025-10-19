from src.lambda_function import lambda_handler
import json
import boto3
from moto import mock_aws

BUCKET_NAME = "my_ingestion_bucket"
file_name = "test_data.csv"
obfuscated_file_name = f"{file_name.split(".")[0]}_obfuscated.{file_name.split(".")[1]}" 

if file_name == "test_data.csv":
    fields_to_obfuscate = ["name", "email_address"]
elif file_name == "gold_price_data.csv":
    fields_to_obfuscate = ["open", "low", "volume"]
else:
    fields_to_obfuscate = []

with open(f"testing_files/{file_name}", "r") as f:
    file_data = f.read()

EVENT = {
    "file_to_obfuscate": f"s3://{BUCKET_NAME}/{file_name}",
    "pii_fields": fields_to_obfuscate
}

with mock_aws():
    # Make fake S3 bucket
    test_client = boto3.client("s3")
    test_client.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
    )

    # Put csv file to obfuscate in fake bucket
    test_client.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=file_data
    )

    # Execute GDPR Obfuscator Lambda handler
    lambda_handler(json.dumps(EVENT), "")

    # Retrieve obfuscated data 
    checking_file = test_client.get_object(
        Bucket=BUCKET_NAME,
        Key=obfuscated_file_name
    )

    # Write obfuscated data into file for checking
    with open(f"checking_files/{obfuscated_file_name}", "w") as f:
        f.write(checking_file['Body'].read().decode("utf-8"))
