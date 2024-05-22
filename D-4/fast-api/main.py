from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv, find_dotenv
import os

def reload_env():
    env_file = find_dotenv('.env.vars')
    if env_file:
        load_dotenv(env_file)
    else:
        print("No .env.vars file found")

reload_env()

app = FastAPI()

# Get environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

# Print environment variables to console for debugging
print("AWS_ACCESS_KEY_ID:", AWS_ACCESS_KEY_ID)
print("AWS_SECRET_ACCESS_KEY:", AWS_SECRET_ACCESS_KEY)
print("AWS_REGION:", AWS_REGION)
print("SQS_QUEUE_URL:", SQS_QUEUE_URL)

# Initialize boto3 SQS client
sqs_client = boto3.client(
    'sqs',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

class LogEntryPayload(BaseModel):
    message: str
    level: str

@app.post("/log")
async def create_log_entry(payload: LogEntryPayload):
    try:
        payload_json = payload.json()
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=payload_json
        )
        return {"message": "Log entry sent to queue", "message_id": response['MessageId']}
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=500, detail="AWS credentials not provided or invalid.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/env")
async def get_env():
    reload_env()
    return {
        "AWS_ACCESS_KEY_ID": os.getenv('AWS_ACCESS_KEY_ID'),
        "AWS_SECRET_ACCESS_KEY": os.getenv('AWS_SECRET_ACCESS_KEY'),
        "AWS_REGION": os.getenv('AWS_REGION'),
        "SQS_QUEUE_URL": os.getenv('SQS_QUEUE_URL')
    }

