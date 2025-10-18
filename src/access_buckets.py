import boto3
import logging
from botocore.exceptions import ClientError


def receive_data(bucket_name: str, key: str) -> str:
    """Receives data from a specific bucket and key

    Returns a string containing the data at the location

    Args:
        bucket_name (str): the name of the bucket
        key (str): the filepath that leads to the data

    Returns:
        output (str): a string of the contained data

    Raises:
        e (ClientError): an informative error message
    """

    s3_client = boto3.client("s3")
    try:
        body = s3_client.get_object(
            Bucket=bucket_name,
            Key=key
        )
        output = body['Body'].read().decode("utf-8")
        return output
    except ClientError as e:
        logging.error(e)
        raise e


def send_data(bucket_name: str, key: str, body_content: str) -> None:
    """Sends data to a specific bucket and key

    Stores a string containing the data at the location

    Args:
        bucket_name (str): the name of the bucket
        key (str): the filepath that leads to the data
        body_content (str): the data to be stored

    Raises:
        e (ClientError): an informative error message
    """

    s3_client = boto3.client("s3")
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=body_content
        )
    except ClientError as e:
        logging.error(e)
        raise e
