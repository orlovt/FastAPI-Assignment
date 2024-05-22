# Dockerized FastAPI and Worker Service

This repository contains a Dockerized FastAPI service and a worker service. The FastAPI service handles incoming HTTP requests, while the worker processes tasks asynchronously. Both services are orchestrated using Docker Compose, both are connected to aws SQS, which was created in `root/cdk-SQS-deployment`. 

## Project Structure

```
.
├── README.md
├── docker-compose.yml
├── fast-api
│   ├── Dockerfile
│   ├── __init__.py
│   ├── main.py
│   └── requirements.txt
├── send_logs.py
└── worker
    ├── Dockerfile
    ├── __init__.py
    ├── main.py
    └── requirements.txt
```

### Directories and Files

- `docker-compose.yml`: Docker Compose file to orchestrate the FastAPI and worker services.
- `fast-api/`: Directory containing the FastAPI service.
  - `Dockerfile`: Dockerfile for building the FastAPI service image.
  - `__init__.py`: Initialization file for the FastAPI service.
  - `main.py`: Main application file for the FastAPI service.
  - `requirements.txt`: Python dependencies for the FastAPI service.
- `send_logs.py`: Script to send logs (assumed functionality).
- `worker/`: Directory containing the worker service.
  - `Dockerfile`: Dockerfile for building the worker service image.
  - `__init__.py`: Initialization file for the worker service.
  - `main.py`: Main application file for the worker service.
  - `requirements.txt`: Python dependencies for the worker service.

## Setup and Running the Services

### Prerequisites

- Docker installed on your machine.
- Docker Compose installed on your machine.

### Steps to Run

1. **Clone the Repository:**

   ```bash
   cd /path/to/docker-api-and-worker
   ```

2. **Build and Start the Services:**

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker images and start the services defined in the `docker-compose.yml` file.

3. **Accessing the FastAPI Service:**

   Once the services are up and running, you can access the FastAPI service at `http://localhost:8000`.

4. **Worker Service:**

   The worker service runs in the background and processes tasks asynchronously. Ensure it is running correctly by checking the Docker container logs.

5. **Run POST requests to FastAPI**
   
   `python send_logs.py`

6. **Check local postgresql db**
   
    ```bash
    psql -U myuser -d test_db

    \dt # should how log_entries 

    SELECT * FROM log_entries;
    ```
   

### Stopping the Services

To stop the services, use the following command:

```bash
docker-compose down
```

### Rebuilding the Services

If you make changes to the code and need to rebuild the images, use the following command:

```bash
docker-compose up --build
```
