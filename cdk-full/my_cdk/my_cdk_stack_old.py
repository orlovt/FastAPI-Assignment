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

        # Create an SQS queue
        queue = sqs.Queue(
            self, "MyQueue",
            visibility_timeout=Duration.seconds(300),
            retention_period=Duration.seconds(500),
        )

        # Create the Lambda function
        lambda_function = _lambda.Function(
            self, "MyLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("fast_api"),
            environment={
                'SQS_QUEUE_URL': queue.queue_url
            },
            memory_size=256,  # Increase memory size
            timeout=Duration.seconds(30)  # Increase timeout
        )

        # Create an API Gateway REST API
        api = apigateway.LambdaRestApi(
            self, "MyApi",
            handler=lambda_function,
            proxy=False
        )

        # Define the /send POST endpoint
        send_resource = api.root.add_resource("send")
        send_resource.add_method("POST")

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
