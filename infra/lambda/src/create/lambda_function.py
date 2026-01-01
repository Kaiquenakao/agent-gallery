import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")

    return {
        "statusCode": 201,
        "body": json.dumps(
            {
                "message": "Agente criado com sucesso na galeria!",
                "received_data": event.get("body"),
            }
        ),
    }
