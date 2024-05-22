#  Local FastAPI

This is a fully local implementation of **FastAPI**

## Project Structure

```
.
├── README.md
├── __pycache__
│   └── main.cpython-38.pyc
├── create_tables.py
├── main.py
├── requirements.txt
└── tests
    ├── __pycache__
    │   └── test_main.cpython-38-pytest-7.1.2.pyc
    └── test_main.py
```

## Files and Directories

- `README.md`: This file, containing an overview of the project.
- `main.py`: The main application file containing the FastAPI app and the database models.
- `create_tables.py`: Script to create the necessary database tables (if not created during startup).
- `requirements.txt`: A list of dependencies required for the project.
- `tests/`: Directory containing test cases for the application.

## Dependencies

The project uses the following main dependencies:

- FastAPI
- SQLAlchemy (with async support)
- asyncpg
- pydantic

You can install these dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Local Database Setup

The database URL is configured in `main.py` as follows:

```python
DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost/test_db"
```
In terminal we have to run:

```bash
psql postgres  # creating postgresql db 

psql (14.12 (Homebrew))
Type "help" for help.

postgres=# CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE ROLE

postgres=# CREATE DATABASE test_db;
CREATE DATABASE

postgres=# GRANT ALL PRIVILEGES ON DATABASE test_db TO myuser;
GRANT

postgres-# \q
```



## Running the Application

To run the application, use the following commands:

1. To initially create tables use: 

```
python create_tables.py
```

2. To run the FastAPI locally: 
```bash
uvicorn main:app --reload
```

- This will start the FastAPI application and make it available at `http://localhost:8000`.


 3. Next we have to send it some requests, in order to do this: 
```
python send_requests.py
```


4. After Sending reuests we can see if they got inserted into the `test_db`

```
psql -U myuser -d test_db


\dt # should how log_entries 


SELECT * FROM log_entries;
```


5. Done



- **Description:** This endpoint creates a new log entry in the database with the specified message and level.

## Database Models

### LogEntry

Represents a log entry in the system.

- `id` (int): The unique identifier for the log entry.
- `message` (str): The message associated with the log entry.
- `level` (str): The level of the log entry (e.g., INFO, WARNING, ERROR).
- `timestamp` (datetime): The timestamp when the log entry was created.

## Asynchronous Database Operations

The application uses SQLAlchemy's async support to handle database operations asynchronously. The `log_entry` function logs an entry with the specified message and level.


## Notes

- Ensure the PostgreSQL server is running and accessible.
- Update the `DATABASE_URL` with your actual database credentials.
- The database tables are created during the application's startup event.
