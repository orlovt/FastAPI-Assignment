from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost/test_db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class LogEntry(Base):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    level = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

async def log_entry(session: AsyncSession, message: str, level: str):
    new_log = LogEntry(message=message, level=level)
    session.add(new_log)
    await session.commit()

app = FastAPI()

class LogEntryPayload(BaseModel):
    message: str
    level: str

@app.post("/log")
async def create_log_entry(payload: LogEntryPayload):
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
