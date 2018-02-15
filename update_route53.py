# import standard libs
import argparse
import json
import re
import urllib
import uuid
import os

# import local libs/modules and external files
# optional import of settings file, if present
try:
    import settings_file
except ImportError:
    pass

# import external/non-standard libs
import boto3


def parse_args():
    """
    Function to interpret and setup arguments flags from user
    """
    # main parser method
    parser = argparse.ArgumentParser(
        # main description of arg when using --help
        # eg: script.py --help
        description="tool to send IP and url to AWS Kinesis, update Route53",
        # usage details when using --help
        usage="python [option] --aws_domain route53domain.com"
              " --ip 1.2.3.4"
              " --check_url http://api.ipify.org"
              " --aws_key reYOURACCESSKEYHEREg"
              " --aws_secret rePUTYOURSUPERSECRETHERETHISISANEXAMPLEr"
              " --aws_region eu-west-1"
              " --aws_stream update-route53"
              " --aws_partition shardId-000000000000"
    )
    # add each argument and options for argument
    # add more argument parsers for more arguments
    parser.add_argument(
        # specify argument
        "--aws_domain",
        # what variable argument will be written to
        dest="domain",
        # text that is returned when using --help
        help="[REQUIRED] route53 zone",
        # default value if arg not specified by user
        # not setting this means arg is required/mandatory
        default=None
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
    parser.add_argument(
        "--aws_key",
        dest="aws_access_key_id",
        help="[REQUIRED] AWS access key ID"
    )
    parser.add_argument(
        "--aws_secret",
        dest="aws_secret_access_key",
        help="[REQUIRED] AWS secret access key"
    )
    parser.add_argument(
        "--aws_region",
        dest="aws_region_name",
        help="[OPTIONAL] AWS region name"
    )
    parser.add_argument(
        "--aws_stream_name",
        dest="aws_stream_name",
        help="[OPTIONAL] AWS kinesis stream name"
    )
    parser.add_argument(
        "--aws_partition_key",
        dest="aws_partition_key",
        help="[OPTIONAL] AWS kinesis stream partition key"
    )
    return parser.parse_args()


def check_domain(domain):
    """
    Function to check DOMAIN is present and valid
    """

    # check if key is present as input var
    if domain:
        print "AWS_DOMAIN variable from arg/flag found!"
        return domain

    # check if key is present as env var
    if os.environ.get("AWS_DOMAIN"):
        print "AWS_DOMAIN variable from ENV found!"
        return os.environ["AWS_DOMAIN"]

    # check if key is present as settings_file
    try:
        if settings_file.AWS_DOMAIN:
            print "AWS_DOMAIN variable from settings_file found!"
            return settings_file.AWS_DOMAIN
    except Exception:
        pass

    # raise exception if domain variable is still nothing
    if not domain or domain is None or domain == "None":
        raise Exception("AWS_DOMAIN not found or specified!")

    # debug print domain
    # print domain

    return domain


def check_ip(check_url, ip=None):
    """
    Function to check IP is present and valid
    """
    # debug print url
    print "Request URL: {}".format(check_url)

    # check if ip is a prescribed variable, or is empty, and go get
    if not ip or ip == "None":
        # check ip
        request = urllib.urlopen(check_url).read()
        # write IP to variable
        ip = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", request)
        # debug print request contents
        # print("Request response: {}").format(request)

        return str(ip[0])

    # check if ip is present
    if ip:
        # if present then just return that
        return ip

    # raise exception if ip is not found
    if not ip:
        raise Exception("IP not found")

    return ip


def check_aws_creds(aws_access_key_id, aws_secret_access_key, aws_region_name):
    """
    Function to check AWS Credentials are present and valid
    """

    # check if key is present as input var
    if aws_access_key_id and aws_secret_access_key and aws_region_name:
        print "aws_access_key_id variable from arg/flag found!"
        print "aws_secret_access_key variable from arg/flag found!"
        print "aws_region variable from arg/flag found!"
        return aws_access_key_id, aws_secret_access_key, aws_region_name

    # check if key is present as env var
    if (os.environ.get("AWS_KEY") and
            os.environ.get("AWS_SECRET") and
            os.environ.get("AWS_KEY")):
        print "AWS_KEY variable from ENV found!"
        print "AWS_SECRET variable from ENV found!"
        print "AWS_REGION variable from ENV found!"
        return (os.environ["AWS_KEY"],
                os.environ["AWS_SECRET"],
                os.environ["AWS_REGION"])

    # check if key is present as settings_file
    try:
        if (settings_file.AWS_ACCESS_KEY_ID and
                settings_file.AWS_SECRET_ACCESS_KEY and
                settings_file.AWS_REGION_NAME):
            print "AWS_ACCESS_KEY_ID from settings_file found!"
            print "AWS_SECRET_ACCESS_KEY from settings_file found!"
            print "AWS_REGION_NAME from settings_file found!"
            return (settings_file.AWS_ACCESS_KEY_ID,
                    settings_file.AWS_SECRET_ACCESS_KEY,
                    settings_file.AWS_REGION_NAME)
    except Exception:
        pass

    return aws_access_key_id, aws_secret_access_key, aws_region_name


def check_kinesis_config(aws_stream_name, aws_partition_key):
    """
    Function to check AWS Kinesis configuration is present and valid
    """

    # check if stream details present as input var
    if aws_stream_name and aws_partition_key:
        print "aws_stream_name variable from arg/flag found!"
        print "aws_partition_key variable from arg/flag found!"
        return aws_stream_name, aws_partition_key

    # check if stream details present as env var
    if (os.environ.get("AWS_STREAM_NAME") and
            os.environ.get("AWS_PARTITION_KEY")):
        print "AWS_STREAM_NAME variable from ENV found!"
        print "AWS_PARTITION_KEY variable from ENV found!"
        return os.environ["AWS_STREAM_NAME"], os.environ["AWS_PARTITION_KEY"]

    # check if stream details present as settings_file
    try:
        if settings_file.AWS_STREAM_NAME and settings_file.AWS_PARTITION_KEY:
            print "AWS_STREAM_NAME variable from settings_file found!"
            print "AWS_PARTITION_KEY variable from settings_file found!"
            return (settings_file.AWS_STREAM_NAME,
                    settings_file.AWS_PARTITION_KEY)
    except Exception:
        pass

    if aws_stream_name is None or "":
        raise Exception("Kinesis Stream Name is invalid")
    if aws_partition_key is None or "":
        raise Exception("Kinesis Partition Key is invalid")

    return aws_stream_name, aws_partition_key


# main function
def main():
    # get default arguments from user, if present
    args = parse_args()

    # check domain
    domain = check_domain(args.domain)

    # check ip, return ip
    ip = check_ip(args.check_url, args.ip)

    # debug print ip
    print "Public IP: {}".format(ip)
    # debug print domain
    print "Target Domain: {}".format(domain)

    # check credentials from file/env/flags, return aws_creds
    aws_creds = check_aws_creds(
        args.aws_access_key_id,
        args.aws_secret_access_key,
        args.aws_region_name
    )
    # debug print creds
    # print aws_creds[0]
    # print aws_creds[1]
    # print aws_creds[2]

    # setup authentication
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html
    # Do not hard code credentials
    # use client autentication
    client = boto3.client(
        'kinesis',
        # Hard coded strings as credentials, not recommended.
        aws_access_key_id=aws_creds[0],
        aws_secret_access_key=aws_creds[1],
        region_name=aws_creds[2]
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
        "domain": domain,
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

    # check and collect kinesis config
    kinesis_config = check_kinesis_config(
        args.aws_stream_name,
        args.aws_partition_key
    )

    # connect to kinesis andput record on stream
    put_record_response = client.put_record(
        StreamName=kinesis_config[0],
        Data=data_message_json,
        PartitionKey=kinesis_config[1]
    )
    # # return response from kinesis
    # print success message
    if put_record_response:
        print "Confirm sent to stream: {}".format(kinesis_config[0])

    return "Kinesis response: {}".format(put_record_response)


# entry point of script here.
# if the context of this environment is called __main__ then run main function.
# this is to make sure that scripts called as secondary modules dont
# misbehave, as importing modules will change the context of __name__
# TIL yo
if __name__ == '__main__':
    main()
