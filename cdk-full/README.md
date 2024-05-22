# CDK Full Deployment

This repository contains a complete setup for deploying a FastAPI service and a worker service using AWS CDK. The setup includes creating an SQS queue and two Lambda functions which import assets from the `fast_api` and `worker` folders.

## Approximate Project Structure

```
.
├── README.md
├── app.py
├── cdk.json
├── fast_api
│   ├── __init__.py
│   ├── lambda_function.py
│   ├── requirements.txt
│   └── venv/
├── my_cdk
│   ├── __init__.py
│   ├── my_cdk_stack.py
├── requirements-dev.txt
├── requirements.txt
├── send_req.py
├── source.bat
└── worker
    ├── __init__.py
    ├── lambda_function.py
    ├── requirements.txt
    └── venv/
```

## Description

This project uses AWS CDK to deploy a FastAPI service and a worker service. It includes the following components:

- **FastAPI service**: Located in the `fast_api` directory.
- **Worker service**: Located in the `worker` directory.
- **AWS CDK**: Used to create the necessary AWS infrastructure, including an SQS queue and two Lambda functions.

## Setup

### Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) configured with your AWS account.
- [AWS CDK](https://aws.amazon.com/cdk/) installed.
- Python 3.x installed.

### Steps to Deploy

1. **Clone the Repository:**

   ```bash
   cd /path/to/cdk-full
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

4. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Synthesize the CloudFormation template:**

   ```bash
   cdk synth
   ```

6. **Deploy the stack:**

   ```bash
   cdk deploy
   ```

### Post Deployment

After deployment, the SQS URL and Lambda function details will be printed in the console. You can also access them via the AWS Management Console.

### Sending Requests

You can use the `send_req.py` script to send requests to the deployed FastAPI service.


### Cleaning Up

To destroy the deployed stack and clean up resources, use the following commands:

```bash
cdk ls # to list the stacks
cdk destroy StackName # to destroy the stack
```

## TODO/Not Completed
- **Add RDS**: Need to add a postgres awd rds to the deployment stack.
- **Logging and Monitoring**: Implement comprehensive logging and monitoring for both the FastAPI and worker services to track performance and errors.
- **Error Handling**: Add robust error handling mechanisms in the FastAPI and worker services.
- **Scalability**: Configure auto-scaling for the Lambda functions to handle varying loads.
- **Security**: Implement security best practices, such as environment variable encryption, IAM roles, and VPC configuration.
- **Unit Tests**: Write comprehensive unit tests for the FastAPI and worker services.
- **Integration Tests**: Implement integration tests to ensure end-to-end functionality of the system.
- **Documentation**: Expand the documentation to include detailed setup instructions, API endpoints, and usage examples.
- **API Gateway**: Configure API Gateway to expose the FastAPI service securely.
- **Load Testing**: Conduct load testing to ensure the system can handle expected traffic and load.
- **Queue Configuration**: Fine-tune the SQS queue configuration for optimal performance.
- **Environment Configuration**: Create different configurations for development, staging, and production environments.
