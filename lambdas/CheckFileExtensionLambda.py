import urllib.parse
import os
import json


def lambda_handler(event, context):
    """Reads event information from EventBridge and extracts and returns filename"""
    print("Received event: " + json.dumps(event, indent=2))
    # Get the object from the event and show its content type
    bucket = event["detail"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["detail"]["object"]["key"], encoding="utf-8")
    filename, file_extension = os.path.splitext(key)
    print(f"File extension is: {file_extension}")
    return {
        'source_bucket': bucket,
        'source_key': key,
        "file_extension": file_extension,
        "filename": filename,
    }
