from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime

def reload_env():
    env_file = find_dotenv('.env.vars')
    if env_file:
        load_dotenv(env_file)
    else:
        print("No .env.vars file found")

# Reload environment variables
reload_env()

app = FastAPI()

# Get environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

# Print environment variables to console for debugging
print("DATABASE_URL:", DATABASE_URL)
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

# Setup SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Define LogEntry model
class LogEntry(Base):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    level = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Define payload model
class LogEntryPayload(BaseModel):
    message: str
    level: str

# Endpoint to log entries
@app.post("/log")
async def create_log_entry(payload: LogEntryPayload):
    try:
        # Print the payload to ensure it's correct
        payload_json = payload.json()
        print(f"Payload to send to SQS: {payload_json}")
        
        # Send message to SQS
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=payload_json
        )
        
        # Print the response from SQS
        print(f"Sent message to SQS: {response}")
        
        # Return the response to the client
        return {"message": "Log entry sent to queue", "message_id": response['MessageId']}
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"AWS credentials error: {e}")
        raise HTTPException(status_code=500, detail="AWS credentials not provided or invalid.")
    except Exception as e:
        print(f"Error sending message to SQS: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get environment variables
@app.get("/env")
async def get_env():
    reload_env()
    return {
        "DATABASE_URL": os.getenv('DATABASE_URL'),
        "AWS_ACCESS_KEY_ID": os.getenv('AWS_ACCESS_KEY_ID'),
        "AWS_SECRET_ACCESS_KEY": os.getenv('AWS_SECRET_ACCESS_KEY'),
        "AWS_REGION": os.getenv('AWS_REGION'),
        "SQS_QUEUE_URL": os.getenv('SQS_QUEUE_URL')
    }

# Startup event to print environment variables
@app.on_event("startup")
async def on_startup():
    reload_env()
    print("DATABASE_URL:", os.getenv('DATABASE_URL'))
    print("AWS_ACCESS_KEY_ID:", os.getenv('AWS_ACCESS_KEY_ID'))
    print("AWS_SECRET_ACCESS_KEY:", os.getenv('AWS_SECRET_ACCESS_KEY'))
    print("AWS_REGION:", os.getenv('AWS_REGION'))
    print("SQS_QUEUE_URL:", os.getenv('SQS_QUEUE_URL'))

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created.")
