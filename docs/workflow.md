# How this app works

This app works in 2 Parts:

* Local part
* AWS Part

## Logging

Logs from the Local Python App are printed to stdout
Logs from Lambda function are also stdout, which is be printed to a CloudWatch Logs stream of the same name as the stream, effectively `/aws/lambda/STREAM_NAME`

## Local Part

The local part of the app, will:

* Receive required data from user:
  * Credentials
  * Target Domain
  * Kinesis stream
* Receive/Determine local public IP
* Format a payload
* Connect to AWS Kinesis
* Post [payload](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html) to Kenesis

Sample Record:

```json
{
    "StreamName": "lambda-update-route53-kareempoc-stream",
    "Data": {"ip": "1.2.3.4","domain": "somedomain.com","uuid": "70e3e22a-e50e-4770-89ae-6f1d95da9b44"},
    "PartitionKey": "shardId-000000000000"
}
```

## AWS Part 1

* The Kinesis stream will store and carry the message payload.
* The lambda function will pickup the message payload.

## AWS Part 2

The lambda function expects to receive a dictionary, with:

* "ip" that is to be set
* "domain" to be updated
* "uuid" of the request, for logging

The event is expected from Kinesis, as a JSON payload.
Expected format:

```code
{
    "ip": 1.2.3.4,
    "domain": somedomain.com,
    "uuid": str(uuid.uuid4())
}
```

The JSON [payload](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_GetRecords.html) is included in a Kinesis event.
Expected format:

```json
{
    u 'Records': [
        {
        u 'eventVersion': u '1.0',
        u 'eventID': u 'shardId-000000000000: 49590637274395895188314144078341336168450725721336184834',
        u 'kinesis': {
            u 'approximateArrivalTimestamp': 1543618890.885,
            u 'partitionKey': u 'shardId-000000000000',
            u 'data': u 'BASE64-ENCODED-PAYLOAD-GOES-HERE',
            u 'kinesisSchemaVersion': u '1.0',
            u 'sequenceNumber': u '49590637274395895188314144078341336168450725721336184834'
            },
        u 'invokeIdentityArn': u 'arn:aws:iam: : 123456789012:role/lambda-update-route53-kareempoc-lambda-role',
        u 'eventName': u 'aws:kinesis:record',
        u 'eventSourceARN': u 'arn:aws:kinesis:eu-west-1: 123456789012:stream/lambda-update-route53-kareempoc-stream',
        u 'eventSource': u 'aws:kinesis',
        u 'awsRegion': u 'eu-west-1'
        }
    ]
}
```

The base64-encoded payload looks something like this:

```code
eyJpcCI6ICIxLjIuMy40IiwgImRvbWFpbiI6ICJzb21lZG9tYWluLmNvbSIsICJ1dWlkIjogImRiZDQyZTRjLWEzOWMtNGFjMC04MjZhLTE2OTBlNjZlZGM3ZSJ9
```

The base64-decoded payload:

```json
{
    "ip": "1.2.3.4",
    "domain": "somedomain.com",
    "uuid": "dbd42e4c-a39c-4ac0-826a-1690e66edc7e"
}
```