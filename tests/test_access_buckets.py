import boto3
from moto import mock_aws
# import pytest
from src.access_buckets import receive_data, send_data
import unittest
from botocore.exceptions import ClientError


class Test_Receive_Data(unittest.TestCase):
    # @pytest.mark.skip
    def test_retrieves_correct_data_1(self):
        # Arrange
        bucket = 'my-bucket-1234'
        body_to_retrieve = "\n".join(
            ["student_id,name,course,cohort," +
             "graduation_date,email_address",
             "1,'John Smith','Software','December'," +
             "'2024-03-31','j.smith@email.com'",
             "2,'Jane Doe','Software','March'," +
             "'1999-08-01','j.doe@email.com'",
             "3,'Mike Jones','Hardware','September'," +
             "'2022-12-21','m.jones@email.com'",
             "4,'Anne White','Mechanics','March'," +
             "'2005-01-29','annepwhite@email.com'"]
             )
        key = 'folder/file.csv'
        # Act
        with mock_aws():
            test_client = boto3.client('s3')
            test_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
            test_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=body_to_retrieve
            )
            resultant_data = receive_data(bucket, key)
        # Assert
        if resultant_data != body_to_retrieve:
            raise AssertionError(
                "Result has not returned correctly"
            )

    # @pytest.mark.skip
    def test_retrieves_correct_data_2(self):

        # Arrange
        body_to_retrieve = "\n".join([
            "student_id,name,course,cohort," +
            "graduation_date,email_address",
            "1,'John Smith','Software','Decembxr'," +
            "'2024703-31','j.smith@email.com'",
            "2,'Jane Doe','Software','Mxrch'," +
            "'1999-08-01','j.doe@email.com'",
            "3,'Mike Jones','Harxware','September'," +
            "'2022-12-21','m.jones@email.com'",
            "4,'Anne White','Mechaxics','March'," +
            "'2005-01-29','annepwhite@email.com'"
        ])
        bucket = 'my-bucket-1234'
        key = 'file_2.csv'
        # Act
        with mock_aws():
            test_client = boto3.client('s3')
            test_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
            test_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=body_to_retrieve
            )
            resultant_data = receive_data(bucket, key)
        # Assert
        if resultant_data != body_to_retrieve:
            raise AssertionError(
                "Result has not returned correctly"
            )

    # @pytest.mark.skip
    def test_key_error_logged_correctly(self):

        # Arrange
        bucket = 'my-bucket-123'
        body_to_retrieve = "\n".join([
            "student_id,name,course,cohort," +
            "graduation_date,email_address",
            "1,'John Smith','Software','Decembxr'," +
            "'2024703-31','j.smith@email.com'",
            "2,'Jane Doe','Software','Mxrch'," +
            "'1999-08-01','j.doe@email.com'",
            "3,'Mike Jones','Harxware','September'," +
            "'2022-12-21','m.jones@email.com'",
            "4,'Anne White','Mechaxics','March'," +
            "'2005-01-29','annepwhite@email.com'"
        ])
        s3_key = 'file_2.csv'
        incorrect_json_key = 'file_2.cv'
        # Act
        with mock_aws():
            test_client = boto3.client('s3')
            test_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
            test_client.put_object(
                Bucket=bucket,
                Key=s3_key,
                Body=body_to_retrieve
            )
            # Assert
            with self.assertRaises(ClientError):
                receive_data(bucket, incorrect_json_key)

    # @pytest.mark.skip
    def test_bucket_error_logged_correctly(self):

        # Arrange
        bucket = 'my-bucket-1234'
        body_to_retrieve = "\n".join([
            "student_id,name,course,cohort," +
            "graduation_date,email_address",
            "1,'John Smith','Software','Decembxr'," +
            "'2024703-31','j.smith@email.com'",
            "2,'Jane Doe','Software','Mxrch'," +
            "'1999-08-01','j.doe@email.com'",
            "3,'Mike Jones','Harxware','September'," +
            "'2022-12-21','m.jones@email.com'",
            "4,'Anne White','Mechaxics','March'," +
            "'2005-01-29','annepwhite@email.com'"
        ])
        key = 'file_2.csv'
        incorrect_bucket = 'my-bucket-123'
        # Act
        with mock_aws():
            test_client = boto3.client('s3')
            test_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
            test_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=body_to_retrieve
            )
        # Assert
            with self.assertRaises(ClientError):
                receive_data(incorrect_bucket, key)


class Test_Send_Data(unittest.TestCase):
    # @pytest.mark.skip
    def test_sends_correct_data_1(self):
        # Arrange
        body = [
            "student_id,name,course,cohort," +
            "graduation_date,email_address",
            "1,'John Smith','Software','Decembxr'," +
            "'2024703-31','j.smith@email.com'",
            "2,'Jane Doe','Software','Mxrch'," +
            "'1999-08-01','j.doe@email.com'",
            "3,'Mike Jones','Harxware','September'," +
            "'2022-12-21','m.jones@email.com'",
            "4,'Anne White','Mechaxics','March'," +
            "'2005-01-29','annepwhite@email.com'"
        ]
        bucket = 'my-bucket-1234'
        body_to_send = "\n".join(body)
        key = 'file_1.csv'
        # Act
        with mock_aws():
            test_client = boto3.client('s3')
            test_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
            send_data(bucket, key, body_to_send)
            resultant_data = test_client.get_object(
                Bucket=bucket,
                Key=key
            )
        # Assert
        if resultant_data['Body'].read().decode("utf-8") != body_to_send:
            raise AssertionError(
                "Result has not returned correctly"
            )

    # @pytest.mark.skip
    def test_sends_correct_data_2(self):

        # Arrange
        bucket = 'my-bucket-5678'
        body_to_send = "\n".join(
            ["student_id,name,course,cohort," +
             "graduation_date,email_address",
             "1,'John Smith','Software','December'," +
             "'2024_03-31','j.smith@email.com'",
             "2,'Jane Doe','Software','March'," +
             "'1999-08-01','j.doe@email.com'",
             "3,'Mike Jones','Hardware','September'," +
             "'2022-12-21','m.jones@email.com'",
             "4,'Anne White','Mechanics','March'," +
             "'2005-01-29','annepwhite@email.com'"]
             )
        key = 'file.csv'
        # Act
        with mock_aws():
            test_client = boto3.client('s3')
            test_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
            send_data(bucket, key, body_to_send)
            resultant_data = test_client.get_object(
                Bucket=bucket,
                Key=key
            )
        # Assert
        if resultant_data['Body'].read().decode("utf-8") != body_to_send:
            raise AssertionError(
                "Result has not returned correctly"
            )

    # @pytest.mark.skip
    def test_bucket_error_logged_correctly(self):
        # Arrange
        bucket = 'my-bucket-5678'
        body_to_send = "\n".join(
            ["student_id,name,course,cohort," +
             "graduation_date,email_address",
             "1,'John Smith','Software','December'" +
             "'2024_03-31','j.smith@email.com'",
             "2,'Jane Doe','Software','March'" +
             "'1999-08-01','j.doe@email.com'",
             "3,'Mike Jones','Hardware','September'" +
             "'2022-12-21','m.jones@email.com'",
             "4,'Anne White','Mechanics','March'" +
             "'2005-01-29','annepwhite@email.com'"]
             )
        key = 'file.csv'
        incorrect_bucket = 'my-bucket-567'
        # Act
        with mock_aws():
            test_client = boto3.client('s3')
            test_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
            # Assert
            with self.assertRaises(ClientError):
                send_data(incorrect_bucket, key, body_to_send)
