import aws_cdk as core
import aws_cdk.assertions as assertions

from queue_intergration.queue_intergration_stack import QueueIntergrationStack

# example tests. To run these tests, uncomment this file along with the example
# resource in queue_intergration/queue_intergration_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = QueueIntergrationStack(app, "queue-intergration")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
