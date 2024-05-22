from fastapi import FastAPI, HTTPException
import boto3
import os
from mangum import Mangum

app = FastAPI()

sqs = boto3.client('sqs')
queue_url = os.getenv('SQS_QUEUE_URL')

@app.post("/send")
async def send_message(message: dict):
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=str(message)
        )
        return {"MessageId": response['MessageId']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)
