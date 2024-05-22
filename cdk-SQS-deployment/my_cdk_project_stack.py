from aws_cdk import core
from aws_cdk import aws_sqs as sqs

class MyCdkProjectStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the SQS queue
        self.queue = sqs.Queue(
            self, "LogQueue",
            visibility_timeout=core.Duration.seconds(300),
        )
