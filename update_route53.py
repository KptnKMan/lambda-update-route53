import argparse
import json
import re
import urllib
import uuid

import settings_file

import boto3


def parse_args():
    parser = argparse.ArgumentParser(
        description="tool to send IP and url to AWS Kinesis, update Route53",
        usage="python [option] --domain route53domain.com"
              " --ip 1.2.3.4"
              " --check_url http://api.ipify.org"
    )
    parser.add_argument(
        "--domain", dest="domain", help="[REQUIRED] route53 zone"
    )
    parser.add_argument(
        "--ip", dest="ip", help="[OPTIONAL] public IP to set in route53"
    )
    parser.add_argument(
        "--check_url",
        dest="check_url",
        help="[OPTIONAL] API URL used to check IP",
        default="https://api.ipify.org"
    )

    return parser.parse_args()


def check_ip(check_url, ip=None):

    # debug print url
    print "Request URL: {}".format(check_url)

    # check if ip is present
    if ip:
        # if present then just return that
        return ip

    # check ip
    request = urllib.urlopen(check_url).read()
    # write IP to variable
    ip = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", request)
    # debug print request contents
    #print("Request response: {}").format(request)

    return str(ip[0])


def main():
    # get default arguments
    args = parse_args()

    # get ip
    ip = check_ip(args.check_url, args.ip)

    # debug print ip
    print "Public IP: {}".format(ip)
    # debug print domain
    print "Target Domain: {}".format(args.domain)

    # setup authentication
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html
    # Do not hard code credentials
    # use client autentication
    client = boto3.client(
        'kinesis',
        # Hard coded strings as credentials, not recommended.
        aws_access_key_id=settings_file.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings_file.AWS_SECRET_ACCESS_KEY,
        region_name=settings_file.AWS_REGION_NAME
    )
    # # debug describe shard from kinesis stream
    # stream_info = client.describe_stream(
    #     StreamName="update-route53",
    #     Limit=1
    # )
    # # debug print kinesis stream description
    # print(stream_info)

    # format message as JSON
    data_message = {
        "ip": ip,
        "domain": args.domain,
        "uuid": str(uuid.uuid4())
    }
    # debug print data message
    # print(data_message)
    # debug print UUID for user
    print "UUID of request: {}".format(data_message.get("uuid"))

    # dump into JSON
    data_message_json = json.dumps(data_message)
    # # debug print
    # print(data_message_json)

    # connect to kinesis andput record on stream
    put_record_response = client.put_record(
        StreamName=settings_file.STREAM_NAME,
        Data=data_message_json,
        PartitionKey=settings_file.PARTITION_KEY
    )
    # # return response from kinesis
    # print success message
    if put_record_response:
        print "Confirm sent to stream: {}".format(settings_file.STREAM_NAME)

    return "Kinesis response: {}".format(put_record_response)


if __name__ == '__main__':
    main()
