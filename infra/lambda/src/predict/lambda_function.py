import json
import logging
import boto3
from boto3.dynamodb.conditions import Key
import openai

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client("ssm")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = ssm.get_parameter(Name="/agent_gallery/table_name", WithDecryption=True)[
    "Parameter"
]["Value"]

OPENAI_API_KEY = ssm.get_parameter(
    Name="/agent_gallery/openai_api_key", WithDecryption=True
)["Parameter"]["Value"]

openai.api_key = OPENAI_API_KEY


def lambda_handler(event, context):
    try:
        agent_id = event.get("agent_id")
        user_message = event.get("message")

        if not agent_id or not user_message:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "agent_id e message são obrigatórios"}),
            }

        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(Key={"agent_id": agent_id})
        agent_item = response.get("Item")

        if not agent_item:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"Agente {agent_id} não encontrado"}),
            }

        prompt = agent_item.get("prompt", "")

        chat_response = openai.ChatCompletion.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message},
            ],
        )

        reply = chat_response["choices"][0]["message"]["content"]

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "agent_id": agent_id,
                    "user_message": user_message,
                    "reply": reply,
                    "status": "success",
                }
            ),
        }

    except Exception as e:
        logger.error(f"Erro ao processar requisição: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
