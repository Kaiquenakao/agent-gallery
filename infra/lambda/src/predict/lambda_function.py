import json


def lambda_handler(event, context):
    input_data = event.get("queryStringParameters", {}).get("input", "default")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "model": "agent-gallery-v1",
                "prediction": f"Resultado processado para: {input_data}",
                "status": "success",
            }
        ),
    }
