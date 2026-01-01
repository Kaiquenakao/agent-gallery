import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client("ssm")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = ssm.get_parameter(Name="/agent_gallery/table_name", WithDecryption=True)[
    "Parameter"
]["Value"]


def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")

    table = dynamodb.Table(TABLE_NAME)
    item = json.loads(event.get("body", "{}"))
    table.put_item(Item=item)

    return {
        "statusCode": 201,
        "body": json.dumps(
            {
                "message": "Agente criado com sucesso na galeria!",
                "received_data": event.get("body"),
            }
        ),
    }
