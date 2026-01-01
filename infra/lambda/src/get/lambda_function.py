import json


def lambda_handler(event, context):
    mock_gallery = [
        {"id": 1, "name": "Agent Alpha", "type": "Assistant"},
        {"id": 2, "name": "Agent Beta", "type": "Predictor"},
    ]

    return {"statusCode": 200, "body": json.dumps(mock_gallery)}
