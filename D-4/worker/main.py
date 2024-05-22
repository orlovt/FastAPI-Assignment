import sys
import os
import asyncio
import boto3
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime
import json
from dotenv import load_dotenv

# Load environment variables from .env.vars file
load_dotenv(dotenv_path='./.env.vars')

DATABASE_URL = os.getenv('DATABASE_URL')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

# Debug prints to verify environment variables
print("Python executable:", sys.executable)
print("Python path:", sys.path)
print("DATABASE_URL:", DATABASE_URL)
print("AWS_ACCESS_KEY_ID:", AWS_ACCESS_KEY_ID)
print("AWS_SECRET_ACCESS_KEY:", AWS_SECRET_ACCESS_KEY)
print("AWS_REGION:", AWS_REGION)
print("SQS_QUEUE_URL:", SQS_QUEUE_URL)

if not SQS_QUEUE_URL:
    raise ValueError("SQS_QUEUE_URL environment variable is not set")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class LogEntry(Base):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    level = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

sqs_client = boto3.client(
    'sqs',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

async def log_entry(session: AsyncSession, message: str, level: str):
    new_log = LogEntry(message=message, level=level)
    session.add(new_log)
    await session.commit()

async def process_message(message_body):
    async with AsyncSessionLocal() as session:
        try:
            payload = json.loads(message_body)
            await log_entry(session, payload['message'], payload['level'])
            print("Log entry created")
        except Exception as e:
            print(f"Error processing message: {e}")

async def poll_sqs():
    while True:
        try:
            print("Polling SQS for messages...")
            response = sqs_client.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20
            )

            print(f"Received response: {response}")

            if 'Messages' in response:
                for message in response['Messages']:
                    print(f"Processing message: {message['Body']}")
                    await process_message(message['Body'])
                    sqs_client.delete_message(
                        QueueUrl=SQS_QUEUE_URL,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    print("Message deleted from queue")
            else:
                print("No messages received")
        except Exception as e:
            print(f"Error polling SQS: {e}")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    # Create the tables before starting to poll SQS
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tables())
    loop.run_until_complete(poll_sqs())
