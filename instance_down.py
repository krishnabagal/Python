#!/usr/bin/env python
import sys
import boto3
import socket
import time


ec2 = boto3.resource('ec2', region_name='ap-south-1')
for instance_id in sys.argv[1:]:
  instance = ec2.Instance(instance_id)
  response = instance.state

for tags in instance.tags:
        if tags["Key"] == 'auto_shutdown':
            instance_auto_shutdown_status = tags["Value"]
        if tags["Key"] == 'deployment':
            instance_deployment_status = tags["Value"]

if instance_auto_shutdown_status == 'true':
    if instance_deployment_status == 'false':
        if instance.state['Name'] == 'running':
            print (str(instance_id) + ': Instance is Already Running..')
        else:
            client = boto3.client('elbv2')
            response = client.register_targets(
            TargetGroupArn='ARN',
                Targets=[
                    {
                      'Id': instance_id ,
                    },
                ],
            )
            print(response)
            time.sleep(60)   
            print(instance.stop())
            print('Stopping your instances: ' + str(instance_id))
    else:
        print ('Application Job is Running...')
else:
    print ('auto_shutdown Instance Tag Is Missing...')
