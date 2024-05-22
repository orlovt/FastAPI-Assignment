from aws_cdk import (
    Stack,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    Duration,
    CfnOutput,
)
from constructs import Construct

class MyCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Components definitions: 
        # 1. SQS Queue
        # 2. FastAPI Lambda function
        # 3. Worker Lambda function

        # Create an SQS queue
        queue = sqs.Queue(
            self, "MyQueue",
            visibility_timeout=Duration.seconds(300),
            retention_period=Duration.seconds(500),
        )

        # Create the FastAPI Lambda function
        fastapi_function = _lambda.Function(
            self, "FastApiFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("fast_api"),
            environment={
                'SQS_QUEUE_URL': queue.queue_url,
            },
            bundling={
                'image': _lambda.Runtime.PYTHON_3_8.bundling_docker_image,
                'command': [
                    'bash', '-c',
                    'pip install -r requirements.txt -t /asset-output && cp -au . /asset-output'
                ]
            },
            memory_size=256,
            timeout=Duration.seconds(30)
        )

        # Create the Worker Lambda function
        worker_function = _lambda.Function(
            self, "WorkerFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("worker"),
            environment={
            'SQS_QUEUE_URL': queue.queue_url,
            },
            bundling={
                'image': _lambda.Runtime.PYTHON_3_8.bundling_docker_image,
                'command': [
                    'bash', '-c',
                    'pip install -r requirements.txt -t /asset-output && cp -au . /asset-output'
                ]
            },
            memory_size=256,
            timeout=Duration.seconds(30)
        )


        # Create an API Gateway REST API for FastAPI
        api = apigateway.LambdaRestApi(
            self, "MyApi",
            handler=fastapi_function,
            proxy=False
        )

        # Define the /log POST endpoint
        log_resource = api.root.add_resource("log")
        log_resource.add_method("POST")

        # Define the /env GET endpoint
        env_resource = api.root.add_resource("env")
        env_resource.add_method("GET")

        # Output the API endpoint
        CfnOutput(
            self, "ApiEndpoint",
            value=api.url,
            description="The URL of the API Gateway endpoint"
        )

        # Output the queue URL
        CfnOutput( 
            self, "QueueURL",
            value=queue.queue_url,
            description="The URL of the SQS Queue"
        )

        CfnOutput(
            self, "Worker",
            value=api.url,
            description="The URL of the API Gateway endpoint"
        )

