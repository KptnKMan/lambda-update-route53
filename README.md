# lambda-update-route53

## Disclaimer

- This is an education repo for me
- There will be a lot of unnecessary comments in my code
- PRs are welcome, if they are useful

## Description

- This is a tool to update a route53 domain using aws kinesis and aws lambda
- There are 3 main components
  - An Update script which checks current public IP and publishes a JSON payload to AWS Kinesis
  - An AWS Kinesis stream that publishes an event to an AWS Lambda function
  - An AWS Lambda function that connects to an AWS Route53 domain/zone
    - The Route53 zone must already exist and be hosted in Route53
    - The Route53 zone is expected to have at least 1 A-Record
    - The A-Record should be a root (eg '*.domain.com' or 'domain.com')

## This repo

- Written in python 2.7.14
- Uses boto3

## Requires/Uses

- AWS Account
- AWS IAM User, access to
  - Post to Kinesis
- AWS IAM Role, access to services:
- AWS Kinesis
- AWS Lambda
- AWS Route53, with a DNS domain registered

## Usage

As an important note, the only required variables are `DOMAIN`, `ACCESS_KEY` and `SECRET_KEY`.
The `IP` variable is always provided manually as an argument, as this is dynamic.
Omitting the `IP` variable will cause the App to query a public service for a public IP.

Local script is run with following syntax:

- `--aws_domain` [REQUIRED] (the target Route53 domain/zone you want to update)
- `--ip` [OPTIONAL] (the IP to update the zone, if manually specified)
- `--check_url` [OPTIONAL] (a URL endpoint that will return the public IP
  - default uses <https://api.ipify.org>)
  - Alternative public endpoints for public IP:
    - <http://checkip.amazonaws.com/>
    - <http://checkip.dyndns.org>
    - <https://ident.me>
- Iam Role(s)
- Kinesis stream
- Lambda function

### Preparing AWS

- setup manually
- run cloudformation
- run terraform

### Preparing App Locally

There are a few methods to prepare and run this app.

- Use runtime args only
- Use runtime args + Environment Variables
- Use runtime args + `settings_file.py`
- Use Docker

The app will check variables in priority order, and will stop checking when a full set is found for each:

- 1st: Use argument flags at runtime
- 2nd: Use Environment Variables
- 3rd: Use a settings_file.py file
- 4th: (Extra) Run it using Docker

### Prep variables

- Using Environment Variables
  - The name fomat of these Environment Variables is designed to not conflict with system defaults
  - List of ENV variables that are checked:

```bash
AWS_DOMAIN="somedomain.com"
AWS_KEY="reYOURACCESSKEYHEREg"
AWS_SECRET="rePUTYOURSUPERSECRETHERETHISISANEXAMPLEr"
AWS_REGION="eu-west-1"
AWS_STREAM_NAME="update-route53"
AWS_PARTITION_KEY="shardId-000000000000"
```

- Using settings_file.py
  - Copy settings_file.example.py to settings_file.py
  - Update settings_file.py with your AWS creds

```python
AWS_DOMAIN = "somedomain.com"
AWS_ACCESS_KEY_ID = "reYOURACCESSKEYHEREg"
AWS_SECRET_ACCESS_KEY = "rePUTYOURSUPERSECRETHERETHISISANEXAMPLEr"
AWS_REGION_NAME = "eu-west-1"
AWS_STREAM_NAME = "update-route53"
AWS_PARTITION_KEY = "shardId-000000000000"
```

### Running the App

- Using argument flags at runtime
  - Usage:

```bash
python [option] \
--aws_domain somedomain.com \
--ip 1.2.3.4 \
--check_url http://api.ipify.org \
--aws_key reYOURACCESSKEYHEREg \
--aws_secret rePUTYOURSUPERSECRETHERETHISISANEXAMPLEr \
--aws_region eu-west-1 \
--aws_stream_name update-route53 \
--aws_partition_key shardId-000000000000
```

- Using Docker
  - This emulates the arguments method internally

```bash
cd lambda-update-route53
# build docker image locally
docker build -t lambda-update-route53 .
# run docker image locally
docker run -it --rm \
--name lambda-update-route53 \
-e AWS_DOMAIN=somedomain.com \
-e IP=1.2.3.4 \
-e AWS_KEY=reYOURACCESSKEYHEREg \
-e AWS_SECRET=rePUTYOURSUPERSECRETHERETHISISANEXAMPLEr \
-e AWS_REGION=eu-west-1 \
-e AWS_STREAM_NAME update-route53 \
-e AWS_PARTITION_KEY shardId-000000000000 \
lambda-update-route53
```

## Todo

- [ ] More detailed instructions
  - [ ] Infra setup
    - [ ] manually?
    - [ ] CloudFormation
    - [ ] Terraform
  - [ ] Prepping variables
  - [ ] Running App
- [ ] Unit tests
- [ ] CloudFormation file
- [ ] Terraform file(s)
- [x] DockerFile
- [ ] dockerhub image automated build
