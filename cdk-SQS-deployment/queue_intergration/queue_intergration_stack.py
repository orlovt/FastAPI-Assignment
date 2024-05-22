from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    aws_sqs as sqs,
)

class QueueIntergrationStack(Stack):
    """
    A class representing a stack for integrating with an SQS queue.
    """

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the SQS queue
        self.queue = sqs.Queue(
            self, "LogQueue",
            visibility_timeout=Duration.seconds(300),
        )
