import boto3

ec2 = boto3.resource('ec2')

instance = ec2.create_instances(
    ImageId='ami-0998bf58313ab53da',
    MinCount=1,
    MaxCount=1,
    InstanceType='t3a.2xlarge',
    KeyName='Fuseki'
)