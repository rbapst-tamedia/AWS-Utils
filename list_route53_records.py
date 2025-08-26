'''List ALL DNS records in route53 zones'''
import boto3

def get_aws_profiles():
    '''Returns the AWS profiles and regions to use'''
    aws_profiles = {
        'unity_demo-admin': 'eu-central-1',
        'unity_dev-admin': 'eu-central-1',
        'unity_preprod-admin': 'eu-central-1',
        'unity_prod-admin': 'eu-central-1',
        'unity_staging-admin': 'eu-central-1',
        }
    return aws_profiles

def get_zones():
    '''Returns the Route53 zones in the AWS account'''
    zones = []
    for zone in boto3.client('route53').list_hosted_zones()['HostedZones']:
        zones.append(zone)
#    print(zones)
    return zones

def get_records(zone_id : str):
    '''Returns the records in a Route53 Zone'''

    route53 = boto3.client('route53')
    records = []
    paginate_resource_record_sets = route53.get_paginator('list_resource_record_sets')

    for record_page in paginate_resource_record_sets.paginate(HostedZoneId = zone_id):
        for record in record_page['ResourceRecordSets']:
            records.append(record)
    return records

def main():
    '''Get Zones are Records in zones and print them'''

    print("Profile\tZone\tId")
    for aws_profile, aws_region in get_aws_profiles().items():
        boto3.setup_default_session(region_name=aws_region, profile_name=aws_profile)
        zones = get_zones()
        for zone in zones:
            print("\t".join([aws_profile, zone['Name'], zone['Id']]))

    print("Zone\tRecords")
    for aws_profile, aws_region in get_aws_profiles().items():
        boto3.setup_default_session(region_name=aws_region, profile_name=aws_profile)
        zones = get_zones()
        for zone in zones:
            records = get_records(zone['Id'])
            for record in records:

                if record.get('ResourceRecords'):
                    for target in record['ResourceRecords']:
                        print("\t".join([zone['Name'], record['Name'], str(record['TTL']), 'IN', record['Type'], target['Value']]))
                elif record.get('AliasTarget'):
                    print("\t".join([zone['Name'], record['Name'], '300', 'IN', record['Type'], record['AliasTarget']['DNSName'], '; ALIAS']))
                else:
                    raise Exception('Unknown record type: {}'.format(record))

if __name__ == "__main__":
    main()
