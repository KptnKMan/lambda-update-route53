# lambda-update-route53

## Disclaimer

- This is an education repo for me
- There will be a lot of unnecessary comments in my code
- PRs are welcome, if they are useful

## Description

- This is a tool to update a route53 domain using a local script, AWS Kinesis and AWS Lambda
- There are 3 main components
  - (1) An AWS Lambda function that modifies/updates an AWS Route53 domain/zone
    - The Route53 zone must already exist and be hosted in Route53
    - The Route53 zone is expected to have at least 1 A-Record
    - The A-Record should be a root (eg '*.domain.com' or 'domain.com')
  - (2) An AWS Kinesis stream that publishes an event to (1) an AWS Lambda function
  - (3) A Local Python App which checks current public IP and publishes a JSON payload to (2) an AWS Kinesis Stream
    - Python App can be run manually in Python
    - Python App can be run as a Docker container
    - Python App can be run as a Kubernetes Helm Chart

## This repo

- Written in python 2.7.14
- Uses boto3

## How this thing works

Details available [here](docs/workflow.md)

## How to use this app

Details available [here](docs/setup.md)

## Todo

- Deployment files
  - [x] DockerFile
  - [ ] DockerHub image automated build
  - [x] Terraform file(s)
  - [ ] Helm Chart
  - [ ] CloudFormation file
- Documentation - Instructions
  - [x] Explain how App works
  - [ ] Infra setup
    - [x] Terraform
    - [ ] CloudFormation
  - [x] Prepping variables
  - [ ] Running App
    - [x] Using Python
    - [x] Using Docker
    - [ ] Using Kubernetes Helm
- Python things
  - [ ] Unit tests
  - [x] Improve cred collection process
  - [x] Properly commented code
  - [ ] Proper internal logging
- Misc/Random