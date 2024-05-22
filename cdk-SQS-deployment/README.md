# CDK SQS

This repository is used to create an AWS SQS (Simple Queue Service) utilizing AWS CDK (Cloud Development Kit).

## Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) configured with your AWS account.
- [AWS CDK](https://aws.amazon.com/cdk/) installed.
- Python 3.x installed.

### Setup

1. **Navigate to the project directory:**

   ```bash
   cd path/to/cdk-SQS-deployment
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

Once AWS SQS is deployed, the SQS URL will be printed in the console. You can also access it via the AWS Management Console.

### Deleting the Stack

To delete the stack, use the following commands:

```bash
cdk ls # to see the list of stacks
cdk destroy StackName # to destroy the stack
```

## Useful Commands

- `cdk ls`          - List all stacks in the app.
- `cdk synth`       - Emit the synthesized CloudFormation template.
- `cdk deploy`      - Deploy this stack to your default AWS account/region.
- `cdk diff`        - Compare the deployed stack with the current state.
- `cdk docs`        - Open CDK documentation.

