from aws_cdk import App
from queue_intergration.queue_intergration_stack import QueueIntergrationStack


def main():
    """
    Entry point of the application.
    """
    app = App()
    QueueIntergrationStack(app, "QueueIntergrationStack")
    app.synth()

if __name__ == "__main__":
    main()
