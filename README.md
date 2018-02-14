# lambda-update-route53

# Disclaimer
- This is an education repo for me
- There will be a lot of unnecessary comments in my code
- PRs are welcome, if they are useful

# Description
- This is a tool to update a route53 domain using aws kinesis and aws lambda
- There are 3 main components
    - An Update script which checks current public IP and publishes a JSON payload to AWS Kinesis
    - An AWS Kinesis stream that publishes an event to an AWS Lambda function
    - An AWS Lambda function that connects to an AWS Route53 domain/zone
        - The Route53 zone must already exist and be hosted in Route53
        - The Route53 zone is expected to have at least 1 A-Record
        - The A-Record should be a root (eg '*.domain.com' or 'domain.com')

# This repo
- Written in python 2.7.14
- Uses boto3

# Requires/Uses
- AWS Account
- AWS IAM User, access to
    - Post to Kinesis
- AWS IAM Role, access to services:
- AWS Kinesis
- AWS Lambda
- AWS Route53, with a DNS domain registered

# Usage
- Prep variables
    - Copy settings_file.example.py to settings_file.py
    - Update settings_file.py with your AWS creds
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_REGION_NAME
    - the other variables do not require modification
- Update Script
    - Script is run with following syntax:
    - -domain [REQUIRED] (the target Route53 domain/zone you want to update)
    - -ip [OPTIONAL] (the IP to update the zone, if manually specified)
    - -check_url [OPTIONAL] (a URL that will return the public IP, default uses 'https://api.ipify.org')
- Iam Role(s)
- Kinesis stream
- Lambda function

# Todo
- More detailed instructions
- Unit tests
- CloudFormation/Terraform file(s)
- DockerFile
- dockerhub image automated build
