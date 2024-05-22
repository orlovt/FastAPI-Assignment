# Assesment Solution

[Link to Assesment](https://docs.google.com/document/d/1qhKdmbC6C4m9gKZ3GWXV12Ljz30SOoFyfrYxOCo8apg/edit#heading=h.8n084zlzrkhc)


## Repo Structure

```
.
├── local-api-with-db
├── cdk-sqs-deployment
├── docker-api-and-worker
└── cdk-full
```

### local-api-with-db

Contains a simple implementation with local **FastAPI** and **postgresqs db**
### cdk-sqs-deployment

Contains a **cdk script** to deploy an **aws sqs** queue. 

### docker-api-and-worker

Cointains a docker-compose which runs **fast-api, worker, postgres db**

### cdk-full

Contains a **cdk script** to deploy: 
  - `fast-api` as a `lambda function`
  - `worker` as a `lambda function`
  - `sqs queue`


### Other instructions: 
- Need configured `aws cli`
- Need running `docker`
- Currently in `docker-api-and-worker` a hardcoded link to `aws sqs`  is used 