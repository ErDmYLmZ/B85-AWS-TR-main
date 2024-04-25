import boto3

client = boto3.client('ec2')

response = client.terminate_instances(
    InstanceIds=[
        'i-0653ef1fe39bbe5e1',
    ],
)

print(response)