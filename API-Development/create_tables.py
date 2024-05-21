from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime
import asyncio

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost/test_db"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class LogEntry(Base):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    level = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
