import json
import logging
import boto3

from boto3.dynamodb.conditions import Key

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

    query_params = event.get("queryStringParameters") or {}
    agent_id = query_params.get("agent_id")
    quero_apenas_prompt = query_params.get("prompt") == "True"

    try:
        if not agent_id:
            logger.info("Executando Scan na tabela...")
            response = table.scan()
            items = response.get("Items", [])
        else:
            logger.info(f"Executando Query para o agent_id: {agent_id}")

            query_kwargs = {"KeyConditionExpression": Key("agent_id").eq(agent_id)}

            if quero_apenas_prompt:
                query_kwargs["ProjectionExpression"] = "prompt"

            response = table.query(**query_kwargs)
            items = response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps(
                    {"message": "Nenhum agente encontrado."}, ensure_ascii=False
                ),
            }

        if agent_id and quero_apenas_prompt:
            resultado = {"prompt": items[0].get("prompt", "")}
        else:
            resultado = items

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(resultado, default=str, ensure_ascii=False),
        }

    except Exception as e:
        logger.error(f"Erro ao acessar DynamoDB: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": f"Erro interno: {str(e)}"}, ensure_ascii=False
            ),
        }
