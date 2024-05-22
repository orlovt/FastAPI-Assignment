from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime


# Define the database URL (localhost, test_db, myuser, mypassword)
DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost/test_db"

# Create the async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the async session local
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Create the base class for the declarative class
Base = declarative_base()

class LogEntry(Base):
    """
    Represents a log entry in the system.

    Attributes:
        id (int): The unique identifier for the log entry.
        message (str): The message associated with the log entry.
        level (str): The level of the log entry (e.g., INFO, WARNING, ERROR).
        timestamp (datetime): The timestamp when the log entry was created.
    """

    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    level = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

async def log_entry(session: AsyncSession, message: str, level: str):
    """
    Logs an entry with the specified message and level.

    Parameters:
    - session (AsyncSession): The async session to use for the database operations.
    - message (str): The message to log.
    - level (str): The level of the log entry.

    Returns:
    None
    """
    new_log = LogEntry(message=message, level=level)
    session.add(new_log)
    await session.commit()

app = FastAPI()

class LogEntryPayload(BaseModel):
    """
    Represents the payload for a log entry.

    Attributes:
        message (str): The log message.
        level (str): The log level.
    """
    message: str
    level: str

@app.post("/log")
async def create_log_entry(payload: LogEntryPayload):
    """
    Create a log entry in the database.

    Args:
        payload (LogEntryPayload): The payload containing the log message and level.

    Returns:
        dict: A dictionary with a success message if the log entry is created.

    Raises:
        HTTPException: If there is an error creating the log entry.
    """
    async with AsyncSessionLocal() as session:
        try:
            await log_entry(session, payload.message, payload.level)
            return {"message": "Log entry created"}
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created.")
