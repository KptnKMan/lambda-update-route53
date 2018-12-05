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
        usage="python [option] --aws_domain somedomain.com"
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
        dest="AWS_DOMAIN",
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
        dest="AWS_ACCESS_KEY_ID",
        help="[REQUIRED] AWS access key ID"
    )
    parser.add_argument(
        "--aws_secret",
        dest="AWS_SECRET_ACCESS_KEY",
        help="[REQUIRED] AWS secret access key"
    )
    parser.add_argument(
        "--aws_region",
        dest="AWS_REGION_NAME",
        help="[OPTIONAL] AWS region name"
    )
    parser.add_argument(
        "--aws_stream_name",
        dest="AWS_STREAM_NAME",
        help="[OPTIONAL] AWS kinesis stream name"
    )
    parser.add_argument(
        "--aws_partition_key",
        dest="AWS_PARTITION_KEY",
        help="[OPTIONAL] AWS kinesis stream partition key"
    )
    return parser.parse_args()


def check_element(element_name, element_var=None,):
    """
    Function designed to check for variable elements for a variety of sources,
    and return that. Checks variable element_name and element_var.
    Example elements:
    aws_domain, aws_access_key_id, aws_secret_access_key,
    aws_region_name, aws_stream_name, aws_partition_key

    Function returns single checked value.
    """

    # print debug element name and variable
    # print "element_name: {}".format(element_name)
    # print "element_var: {}".format(element_var)

    # check if element_var is present as input var
    if element_var:
        print "{} found from arg/flag!".format(element_name)
        return element_var

    # check if element_var is present as ENV var
    if os.environ.get("{}".format(element_name)):
        print "{} found from ENV variable!".format(element_name)
        return os.environ["{}".format(element_name)]

    # check if element_var is present as settings_file
    try:
        if getattr(settings_file, element_name, None):
            print "{} found from settings_file!".format(element_name)
            return getattr(settings_file, element_name, None)
    except Exception:
        pass

    # raise exception if element_var variable is still nothing
    if not element_var or element_var is None or element_var == "None":
        raise Exception("{} not found or specified!".format(element_name))

    return element_var


def check_ip(check_url, ip=None):
    """
    Function to check IP is present and valid
    """
    # debug print url
    print "IP requested from URL: {}".format(check_url)

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


# main function
def main():
    # get default arguments from user, if present
    args = parse_args()

    # check ip, return ip
    ip = check_ip(args.check_url, args.ip)

    # check domain
    domain = check_element("AWS_DOMAIN", args.AWS_DOMAIN)

    # check credentials from file/env/flags, return aws_creds
    aws_key = check_element("AWS_ACCESS_KEY_ID", args.AWS_ACCESS_KEY_ID)
    aws_secret = check_element("AWS_SECRET_ACCESS_KEY", args.AWS_SECRET_ACCESS_KEY)
    aws_region = check_element("AWS_REGION_NAME", args.AWS_REGION_NAME)

    # get kinesis config from file/env/flags
    aws_stream_name = check_element("AWS_STREAM_NAME", args.AWS_STREAM_NAME)
    aws_partition_key = check_element("AWS_PARTITION_KEY", args.AWS_PARTITION_KEY)

    # setup authentication
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html
    # Do not hard code credentials
    # use client autentication
    client = boto3.client(
        'kinesis',
        # Hard coded strings as credentials, not recommended.
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        region_name=aws_region
    )

    # debug describe shard from kinesis stream
    # stream_info = client.describe_stream(
    #     StreamName="update-route53",
    #     Limit=1
    # )
    # debug print kinesis stream description
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
    # debug print ip
    print "Public IP returned: {}".format(ip)
    # debug print domain
    print "Update target DNS record: {}".format(domain)

    # dump into JSON
    data_message_json = json.dumps(data_message)
    # debug print
    # print(data_message_json)

    """
    Sample Record:

    {
        "StreamName": "lambda-update-route53-kareempoc-stream",
        "Data": {"ip": "1.2.3.4","domain": "somedomain.com","uuid": "70e3e22a-e50e-4770-89ae-6f1d95da9b44"},
        "PartitionKey": "shardId-000000000000"
    }
    """

    # connect to kinesis andput record on stream
    put_record_response = client.put_record(
        StreamName=aws_stream_name,
        Data=data_message_json,
        PartitionKey=aws_partition_key
    )

    # return response from kinesis
    # print success message
    if put_record_response:
        print "Confirm sent to stream: {}".format(aws_stream_name)

    return "Kinesis response: {}".format(put_record_response)


# entry point of script here.
# if the context of this environment is called __main__ then run main function.
# this is to make sure that scripts called as secondary modules dont
# misbehave, as importing modules will change the context of __name__
# TIL yo
if __name__ == '__main__':
    main()
