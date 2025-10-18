from lambda_function import lambda_handler
import json
import boto3
from moto import mock_aws


def test_incorrect_json_event():
    # Arrange
    event = ""
    # Act
    response = lambda_handler(event, "")
    # Assert
    if response['statusCode'] != 400:
        raise AssertionError(
            "Status code should be 400"
        )


def test_incorrect_dict_event():
    # Arrange
    event = {}
    # Act
    response = lambda_handler(event, "")
    # Assert
    if response['statusCode'] != 400:
        raise AssertionError(
            "Status code should be 400"
        )


def test_incorrect_json_list():
    # Arrange
    event = ["One", "Two"]
    # Act
    response = lambda_handler(json.dumps(event), "")
    # Assert
    if response["statusCode"] != 400:
        raise AssertionError(
            "Status code should be 400"
        )


def test_incorrect_json_keys():
    # Arrange
    event = {
        "One": "eins",
        "Two": "zwei"
    }
    # Act
    response = lambda_handler(json.dumps(event), "")
    # Assert
    if response["statusCode"] != 400:
        raise AssertionError(
            "Status code should be 400"
        )


def test_incorrect_dict_keys():
    # Arrange
    event = {
        "One": "eins",
        "Two": "zwei"
    }
    # Act
    response = lambda_handler(event, "")
    # Assert
    if response["statusCode"] != 400:
        raise AssertionError(
            "Status code should be 400"
        )


def test_one_incorrect_json_key():
    # Arrange
    event = {
        "file_to_obfuscate": "eins",
        "Two": "zwei"
    }
    # Act
    response = lambda_handler(json.dumps(event), "")
    # Assert
    if response["statusCode"] != 400:
        raise AssertionError(
            "Status code should be 400"
        )


def test_one_incorrect_dict_key():
    # Arrange
    event = {
        "file_to_obfuscate": "eins",
        "Two": "zwei"
    }
    # Act
    response = lambda_handler(event, "")
    # Assert
    if response["statusCode"] != 400:
        raise AssertionError(
            "Status code should be 400"
        )


def test_incorrect_values_in_json():
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
    event = {
        "file_to_obfuscate": "eins",
        "pii_fields": "zwei"
    }
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
        response = lambda_handler(json.dumps(event), "")
    # Assert
    if response["statusCode"] != 400:
        raise AssertionError(
            "Status code should be 400"
        )


def test_incorrect_values_in_dict():
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
    event = {
        "file_to_obfuscate": "eins",
        "pii_fields": "zwei"
    }
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
        response = lambda_handler(event, "")
    # Assert
    if response["statusCode"] != 400:
        raise AssertionError(
            "Status code should be 400"
        )


def test_correct_values_in_json():
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
    event = {
        "file_to_obfuscate": "s3://my_ingestion_bucket/test_1.csv",
        "pii_fields": ["name", "email_address"]
    }
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
        response = lambda_handler(json.dumps(event), "")
    # Assert
    if response["statusCode"] != 200:
        raise AssertionError(
            "Status code should be 200"
        )


def test_correct_values_in_dict():
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
    event = {
        "file_to_obfuscate": "s3://my_ingestion_bucket/test_1.csv",
        "pii_fields": ["name", "email_address"]
    }
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
        response = lambda_handler(event, "")
    # Assert
    if response["statusCode"] != 200:
        raise AssertionError(
            "Status code should be 200"
        )
