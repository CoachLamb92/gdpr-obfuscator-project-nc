import json
import logging
from src.main import obfuscate


def lambda_handler(event: str | dict, context) -> dict:
    """
    AWS Lambda entrypoint.

    Expects event as JSON string or Python dict, with keys:
    - file_to_obfuscate: str
    - pii_fields: str

    Args:
        event (str | dict): input data as an event
        context (any) : unused

    Returns:
        (dict): Response dict
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if isinstance(event, str):
        try:
            event = json.loads(event)
        except Exception as e:
            logger.error("Invalid event: %s", e)
            return {
                "statusCode": 400,
                "body": json.dumps({"error": str(e)})
            }

    if not isinstance(event, dict):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Incorrect event format"})
        }

    if not set(["file_to_obfuscate", "pii_fields"]).issubset(event.keys()):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing keys in event"})
        }

    event = json.dumps(event)

    try:
        obfuscate(event)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Successfully obfuscated data"})
        }
    except Exception as e:
        logger.error("Lambda execution failed: %s", e)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
