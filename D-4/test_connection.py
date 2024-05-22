import asyncio
import asyncpg
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:<password>@database-1.c58s26mwcdf0.us-east-2.rds.amazonaws.com:5432/postgres')

async def test_connection():
    try:
        # Extract the connection URL without the 'postgresql+asyncpg://' prefix
        connection_url = DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')

        # Connect to the database
        conn = await asyncpg.connect(connection_url)
        print("Connection successful!")
        
        # Optionally, perform a simple query to verify the connection
        result = await conn.fetch('SELECT 1')
        print("Query result:", result)

        # Close the connection
        await conn.close()
    except Exception as e:
        print("Connection failed:", str(e))

if __name__ == "__main__":
    asyncio.run(test_connection())
