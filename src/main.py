import json
from src import csv_func, access_buckets
import logging
from botocore.exceptions import BotoCoreError, ClientError


def obfuscate(input: str) -> None:
    """Obfuscates data

    Receives a JSON string containing the location of data (bucket and key) and
    the column headers of the data that require obfuscation. Leaves the initial
    data as is, but creates a second body of obfuscated data with a similarly-
    named key in the same bucket.

    Args:
        input (str): a string in JSON format, containing data location
                     and column headers of data to obfuscate
    """

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    input_dict = json.loads(input)

    s3_address = input_dict["file_to_obfuscate"]
    fields_to_obfuscate = input_dict["pii_fields"]

    # Identify file type
    path_parts = s3_address.split("/")
    bucket_name = path_parts[2]
    file_path = "/".join(path_parts[3:])
    file_type = file_path.split(".")[-1]
    new_file_name = file_path.split(".")[0] + "_obfuscated." + file_type
    try:
        data = access_buckets.receive_data(bucket_name, file_path)
        output_data = csv_func.obfuscate(data, fields_to_obfuscate)
        access_buckets.send_data(
            bucket_name, new_file_name, output_data
        )
        logger.info("Obfuscation successful: %s", new_file_name)
    except (BotoCoreError, ClientError) as e:
        logger.error("Failed to complete obfuscation: %s", e)
