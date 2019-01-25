#!/usr/bin/python3
# Use like: python3 ./listLinuxAmis.py |grep Linux|sort
import boto3
import json

ec2 = boto3.resource('ec2', region_name='eu-west-1')
redhat_owner='309956199498' # from https://access.redhat.com/articles/2962171

filters=[#{'Name': 'description', 'Values': ['Amazon Linux AMI*']},
    {'Name': 'architecture', 'Values': ['x86_64']},
    {'Name': 'owner-id', 'Values': [redhat_owner]}]
images = ec2.images.filter(Filters=filters).all()
for i in images:
    print(i.creation_date, i.id, i.name, i.description)
