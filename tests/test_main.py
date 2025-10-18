from src.main import obfuscate
import boto3
from moto import mock_aws
import sys
import logging
import time


def test_whole_program_with_csv():
    # Arrange
    input_data_list = [
        "student_id,name,course,cohort," +
        "graduation_date,email_address",
        "1,'John Smith','Software','December'," +
        "'2024-03-31','j.smith@email.com'",
        "2,'Jane Doe','Software','March'," +
        "'1999-08-01','j.doe@email.com'",
        "3,'Mike Jones','Hardware','September'," +
        "'2022-12-21','m.jones@email.com'",
        "4,'Anne White','Mechanics','March'," +
        "'2005-01-29','annepwhite@email.com'"
        ]
    expected_data_list = [
        "student_id,name,course,cohort,graduation_date,email_address",
        "1,'***','Software','December','2024-03-31','***'",
        "2,'***','Software','March','1999-08-01','***'",
        "3,'***','Hardware','September','2022-12-21','***'",
        "4,'***','Mechanics','March','2005-01-29','***'"
    ]
    with open("testing_files/test_1.json", "r") as f:
        input_json = f.read()
    expected_data = "\n".join(expected_data_list)
    # Act
    with mock_aws():
        test_client = boto3.client("s3")
        test_client.create_bucket(
                Bucket="my_ingestion_bucket",
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
        test_client.put_object(
                Bucket="my_ingestion_bucket",
                Key="test_1.csv",
                Body="\n".join(input_data_list)
                )
        obfuscate(input_json)
        result = test_client.get_object(
            Bucket="my_ingestion_bucket",
            Key="test_1_obfuscated.csv"
        )
    # Assert
    if result["Body"].read().decode("utf-8") != expected_data:
        raise AssertionError(
            "Result has not returned correctly"
            )


def test_time_taken_with_one_mb_csv():
    # Arrange
    with open("testing_files/test_2.json", "r") as f:
        input_json = f.read()

    with open("testing_files/gold_price_data.csv", "r") as f:
        gold_data = f.read()
    # Act
    with mock_aws():
        test_client = boto3.client("s3")
        test_client.create_bucket(
                Bucket="my_ingestion_bucket",
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
        test_client.put_object(
                Bucket="my_ingestion_bucket",
                Key="gold_price_data.csv",
                Body=gold_data
                )
        start = time.time()
        obfuscate(input_json)
        end = time.time()
    time_taken = end - start
    # Assert
    if sys.getsizeof(gold_data) <= 1000000:
        raise AssertionError(
            "File is not larger than 1MB"
            )
    if time_taken >= 60:
        raise AssertionError(
            "Process took longer than 1 minute"
            )


def test_correct_csv_extension_log(caplog):
    # Arrange
    caplog.set_level(logging.INFO)
    with open("testing_files/test_2.json", "r") as f:
        input_json = f.read()

    with open("testing_files/gold_price_data.csv", "r") as f:
        gold_data = f.read()

    bucket = "my_ingestion_bucket"
    key = "gold_price_data.csv"
    # Act
    with mock_aws():
        test_client = boto3.client("s3")
        test_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
        test_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=gold_data
                )
        obfuscate(input_json)
    # Assert
    if len(caplog.records) != 2:
        raise AssertionError(
            "More or less than 2 logs have been detected"
        )
    if caplog.records[1].levelname != "INFO":
        raise AssertionError(
            "The log detected is not of type: INFO"
        )
    if caplog.records[1].message != (
        "Obfuscation successful: gold_price_data_obfuscated.csv"
    ):
        raise AssertionError(
            "The wrong information has been logged"
        )


def test_incorrect_key(caplog):
    # Arrange
    caplog.set_level(logging.ERROR)
    with open("testing_files/test_2.json", "r") as f:
        input_json = f.read()

    with open("testing_files/gold_price_data.csv", "r") as f:
        gold_data = f.read()
    bucket = "my_ingestion_bucket"
    key = "gold_price_dta.csv"
    # Act
    with mock_aws():
        test_client = boto3.client("s3")
        test_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
        test_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=gold_data
                )
        obfuscate(input_json)
    # Assert
    if len(caplog.records) != 2:
        raise AssertionError(
            "More or less than 2 logs have been detected"
        )
    if caplog.records[1].levelname != "ERROR":
        raise AssertionError(
            "The log detected is not of type: ERROR"
        )
    if caplog.records[1].message != (
        "Failed to complete obfuscation: An error occurred (NoSuchKey) " +
        "when calling the GetObject operation: " +
        "The specified key does not exist."
    ):
        raise AssertionError(
            "The wrong error has been logged"
        )


def test_incorrect_bucket(caplog):
    # Arrange
    caplog.set_level(logging.ERROR)
    with open("testing_files/test_2.json", "r") as f:
        input_json = f.read()

    with open("testing_files/gold_price_data.csv", "r") as f:
        gold_data = f.read()
    bucket = "my_ingion_bucket"
    key = "gold_price_data.csv"
    # Act
    with mock_aws():
        test_client = boto3.client("s3")
        test_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
        test_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=gold_data
                )
        obfuscate(input_json)
    # Assert
    if len(caplog.records) != 2:
        raise AssertionError(
            "More or less than 2 logs have been detected"
        )
    if caplog.records[1].levelname != "ERROR":
        raise AssertionError(
            "The log detected is not of type: ERROR"
        )
    if caplog.records[1].message != (
        "Failed to complete obfuscation: " +
        "An error occurred (NoSuchBucket) when calling the GetObject " +
        "operation: The specified bucket does not exist"
    ):
        raise AssertionError(
            "The wrong error has been logged"
        )
