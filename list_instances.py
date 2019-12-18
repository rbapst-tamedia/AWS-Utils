'''List IP addresses of the EC2 belonging to the web application ASG'''
import boto3

def get_instances():
    '''Returns the EC2 instances in the AWS account'''
    instances = []
    for ec2 in boto3.client('ec2').describe_instances()['Reservations']:
        for instance in ec2['Instances']:
            instances.append(instance)
    return instances

def get_tag_value(tag_name, tags):
    '''Get value of tag named 'tag_name' in tags'''
    for tag in tags:
        if tag['Key'] == tag_name:
            return tag['Value']
    return ''

def get_instance_info(instance_id):
    '''Returns some info from the 'instance_id' EC2 instance'''
    info = {}
    for reservation in (
            boto3
            .client('ec2', region_name='eu-west-1')
            .describe_instances(InstanceIds=[instance_id])
            ['Reservations']
        ):
        for instance in reservation['Instances']:
            info['PrivateIpAddress'] = instance['PrivateIpAddress']
            info['State'] = instance['State']['Name']
            info['Name'] = get_tag_value('Name', instance['Tags'])
    return info

print('InstanceId\tName\tState\tPrivateIp')
for i in get_instances():
    instance_info = get_instance_info(i['InstanceId'])
    print(i['InstanceId']  +
          "\t" + instance_info['Name'] +
          "\t" + instance_info['State'] +
          "\t" + instance_info['PrivateIpAddress'])
