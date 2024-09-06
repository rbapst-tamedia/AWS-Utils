#!/usr/bin/python3
# Use like: python3 ./listWindowsAmis.py |grep Windows|sort
import boto3
import json

ec2 = boto3.resource('ec2')
filters=[#{'Name': 'description', 'Values': ['Microsoft*']},
    {'Name': 'architecture', 'Values': ['x86_64']},
    {'Name': 'root-device-type', 'Values': ['ebs']},
    {'Name': 'block-device-mapping.volume-type', 'Values': ['gp2']},
    {'Name': 'virtualization-type', 'Values': ['hvm']},
    {'Name': 'owner-alias', 'Values': ['amazon']}]
images = ec2.images.filter(Filters=filters).all()
for i in images:
    print(i.creation_date, i.id, i.name, i.description)
