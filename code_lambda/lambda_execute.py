import boto3
import base64
import json
import traceback


"""
AWS Lambda script to update A-Records in AWS Route 53.
Script expects to recieve a dictionary, with:
"ip" that is to be set
"domain" to be updated
"uuid" of the request, for logging

The event is expected from Kinesis, as a JSON payload.
Expected format:
{
    "ip": 1.2.3.4,
    "domain": somedomain.com,
    "uuid": str(uuid.uuid4())
}
"""


# main entry point
def lambda_handler(event, context):
    try:
        # print raw event
        print "Event: {}".format(event)

        # check if event is present
        if not event:
            raise ValueError("Kenesis event not found")

        # run/parse kinesis event through function
        # get back IP and target domain
        ip, domain, uuid = get_ip_domain(event)

        # check if domain name
        if not domain:
            raise ValueError("Domain name is missing/invalid")

        # check for valid IP
        if not ip:
            raise ValueError(
                "IP is not found for {}".format(domain)
            )

        # debug print IP and domain details
        print "IP: {} Domain: {}".format(ip, domain)

        # get zone ID of hosted zone
        # run domain name through function
        # get back zone ID
        route53_zone_id = get_route53_zone_id(domain)
        print "Zone id for {}: {}".format(domain, route53_zone_id)

        # check for valid zone ID
        if not route53_zone_id:
            raise ValueError(
                "Zone ID is not found for {}".format(domain)
            )
        # get list of route53 records
        route53_record_sets_data = get_route53_record_sets(route53_zone_id)
        # debug print route53 records
        print "Route53 Records: {}".format(route53_record_sets_data)

        # check if record set list is valid
        if not route53_record_sets_data:
            raise ValueError("The list of record sets is empty/invalid")
        # compare route53 records with IP data
        # if different:
            # check if records exist
            # if does not exist, create
            # if exist, update with new value
        # generate new change data
        route53_record_sets_changed = change_route53_record_sets(
            ip, route53_record_sets_data
        )
        # debug print changes to make
        print "Route53 Changed Request: {}".format(
            route53_record_sets_changed
        )

        # update record set
        route53_record_sets_response = update_route53_record_sets(
            route53_zone_id, route53_record_sets_changed
        )
        # debug print response of change
        print "Route53 Change Response: {}".format(
            route53_record_sets_response
        )
        # debug print original request UUID
        print "Request UUID: {}".format(uuid)

    # format an exception output
    except:
        # print(error)
        traceback.print_exc()


# function return IP
def get_ip_domain(event):
    # dictionary is returned
    # extract data list
    event_records = event.get("Records")

    # check if list is populated
    if not event_records:
        # raise error if Records not found in event
        raise ValueError("Records not found in event")

    # extract item from list
    event_record = event_records[0]

    # item is dictionary, extract data
    kinesis_data = event_record.get("kinesis")

    # check if item is populated
    if not kinesis_data:
        # raise error if no kinesis data found
        raise ValueError("Value not found from Kinesis data field")

    # extract data field from kinesis data
    base64_encoded_data = kinesis_data.get("data")

    # check if data field is valid/present
    if not base64_encoded_data:
        raise ValueError("Value not found in Kenesis Data field")

    # print(kinesis_data)
    # print(base64_encoded_data)

    # decode data to string
    decoded_data = base64.b64decode(base64_encoded_data)

    # decode base64-encoded data
    print("Base64 encoded: {}").format(decoded_data)

    # decode JSON
    decoded_data_json = json.loads(decoded_data)

    # print JSON decoded data
    print("JSON decoded: {}").format(decoded_data_json)

    # return list
    return (
        decoded_data_json.get("ip"),
        decoded_data_json.get("domain"),
        decoded_data_json.get("uuid")
    )


# get hosted zone ID
def get_route53_zone_id(hosted_zone_name):
    # boto client
    route53_client = boto3.client('route53')

    # get zone details
    zone_details = route53_client.list_hosted_zones_by_name(
        DNSName=hosted_zone_name
    )
    # debug print zone details
    print "Zone details: {}".format(zone_details)

    # dictionary is returned
    # extract data list
    zone_records = zone_details.get("HostedZones")

    # validate if list populated
    if not zone_records:
        raise ValueError("Cannot find zone records")

    print zone_records

    # list of comprehension against zone ids
    record_zone_id = [
        # get the value from id and split it by / and get last value in list
        zone_record.get("Id").split("/")[-1]
        # for the list object/item
        for zone_record
        # in the list of objects
        in zone_records
        # if the Name field matches the target_zone_name
        if zone_record.get("Name") == hosted_zone_name+"."
        # and the Id field is present/valid
        and zone_record.get("Id")
    ]

    # debug print record_zone_id
    print "Zone ID: {}".format(record_zone_id)

    return record_zone_id[0]


# function get route53 records
def get_route53_record_sets(hosted_zone_id):
    # boto client
    route53_client = boto3.client('route53')

    # get list of records
    record_sets = route53_client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id
    )

    # check list of records
    if not record_sets:
        raise ValueError("Records not found!")
    # debug print zone data
    print "List of Records: {}".format(record_sets)

    # list comprehension against records:
    # expression
    # for item in list
    # condition
    record_sets_data = [
        record_set
        for record_set in record_sets.get("ResourceRecordSets")
        if record_set.get("Type") == "A"
    ]

    # return list of records
    return record_sets_data


def change_route53_record_sets(ip, record_sets_data):
    # compare new IP to current IP
    # list comprehension against records:
    record_sets_data_change = [
        record_set
        for record_set in record_sets_data
        if record_set.get("ResourceRecords")[0].get("Value") != ip
    ]

    # change data in each list item
    # replace IP with new IP
    for record in record_sets_data_change:
        record['ResourceRecords'] = [{
            'Value': ip
        }]

    return record_sets_data_change


def update_route53_record_sets(hosted_zone_id, record_sets_data):
    # check if record sets are valid/present
    if not record_sets_data:
        raise ValueError("Record sets data is invalid/missing")

    # boto client
    route53_client = boto3.client('route53')

    # generate change request
    # list comprehension against records:
    change_data = [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": change
        }
        for change in record_sets_data
    ]

    # publish change
    change_response = route53_client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            "Comment": "lambda update-route53",
            "Changes": change_data
        }
    )

    if change_response:
        print "Confirm Updated domain ID: {}".format(hosted_zone_id)

    return change_response
