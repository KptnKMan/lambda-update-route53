# How to use this app

## Requirements

### You Require

- AWS Account
- AWS IAM User with FullAdmin permissions to at least:
  - AWS IAM
  - AWS Kinesis
  - AWS Lambda
  - AWS Route53
  - AWS CloudWatch Logs
- A domain, already managed as a "Hosted Zone" in Route53

### The Kinesis Stream Requires

- AWS Kinesis
  - Access to post to Lambda

### The Lambda Python Function Requires

- AWS IAM Role, access to:
  - Read from AWS Kinesis
- AWS IAM Role, access to services:
  - AWS Kinesis
  - AWS Lambda
  - AWS Route53, with a DNS domain registered
  - AWS CloudWatch Logs

### The Local Python App Requires

- AWS IAM credentials keys
  - Post to AWS Kinesis

## Preparing AWS

### setup manually

TBC at some point, but this really example really is intended to use CloudFormation or Terraform.

Don't expect manual instructions any time soon.

### Create Env via Cloudformation

TBC.

### Create Env via Terraform

TL;DR instructions

- Tools

You need to [Install Terraform](https://learn.hashicorp.com/terraform/getting-started/install.html)

This project is tested with Terraform v0.11.10

- Perpare Variables

The basic variables you need to specify are:

```bash
export TF_VAR_aws_access_key=reYOURACCESSKEYHEREg
export TF_VAR_aws_secret_key=rePUTYOURSUPERSECRETHERETHISISANEXAMPLEr
export TF_VAR_aws_region=eu-west-1
```

- Apply/Build Environment

```bash
terraform get terraform
terraform init terraform
terraform apply -input=false -state="config/project.state" -var-file="config/project.tfvars" "terraform"
```

- Destroy Environment

```bash
terraform destroy -input=false -state="config/project.state" -var-file="config/project.tfvars" "terraform"
```

## Local App Usage

As an important note, the only required variables are `DOMAIN`, `ACCESS_KEY` and `SECRET_KEY`.
The `IP` variable is always provided manually as an argument, as this is dynamic.
Omitting the `IP` variable will cause the App to query a public service for a public IP.

Local script is run with following syntax:

- `--aws_key` [REQUIRED] AWS access key ID
- `--aws_secret` [REQUIRED] AWS secret access key
- `--aws_domain` [REQUIRED] the target Route53 domain/zone you want to update
- `--aws_region` [OPTIONAL] AWS region name
- `--aws_stream_name` [OPTIONAL] AWS kinesis stream name
- `--aws_partition_key` [OPTIONAL] AWS kinesis stream partition key
- `--ip` [OPTIONAL] the IP to update the zone, if manually specified
- `--check_url` [OPTIONAL] a URL endpoint that will return the public IP

Notes:

- `ip` only if you want to sepcify a custom IP
- `aws_domain` A-Records only, subdomains work!
- `check_url` default uses <https://api.ipify.org>)
- Alternative public endpoints for public IP:
  - <http://checkip.amazonaws.com/>
  - <http://checkip.dyndns.org>
  - <https://ident.me>

### Preparing App Locally

There are a few methods to prepare and run this app.
The app will check variables in priority order, and will stop checking each variable order when a full set is found.
This means that you can use variables from different sources.

- Use runtime args only
- Use runtime args + Environment Variables
- Use runtime args + Environment Variables + `settings_file.py`
- Use Docker, the app can also be run using Docker.

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
--aws_stream_name lambda-update-route53-kareempoc-stream \
--aws_partition_key shardId-000000000000
```

- Using Environment Variables
  - The name fomat of these Environment Variables is designed to not conflict with system defaults
  - List of ENV variables that are checked:

```bash
AWS_DOMAIN="somedomain.com"
AWS_ACCESS_KEY_ID="reYOURACCESSKEYHEREg"
AWS_SECRET_ACCESS_KEY="rePUTYOURSUPERSECRETHERETHISISANEXAMPLEr"
AWS_REGION_NAME="eu-west-1"
AWS_STREAM_NAME="lambda-update-route53-kareempoc-stream"
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
AWS_STREAM_NAME = "lambda-update-route53-kareempoc-stream"
AWS_PARTITION_KEY = "shardId-000000000000"
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
-e AWS_ACCESS_KEY_ID=reYOURACCESSKEYHEREg \
-e AWS_SECRET_ACCESS_KEY=rePUTYOURSUPERSECRETHERETHISISANEXAMPLEr \
-e AWS_REGION_NAME=eu-west-1 \
-e AWS_STREAM_NAME lambda-update-route53-kareempoc-stream \
-e AWS_PARTITION_KEY shardId-000000000000 \
lambda-update-route53
```