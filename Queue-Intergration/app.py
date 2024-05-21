from aws_cdk import App
from queue_intergration.queue_intergration_stack import QueueIntergrationStack

app = App()
QueueIntergrationStack(app, "QueueIntergrationStack")
app.synth()
