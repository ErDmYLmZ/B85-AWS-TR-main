
import boto3
client = boto3.client('s3')

response = client.delete_object(
    Bucket='testing-bucket-techpro',
    Key='putobj.py',
)

print(response)
# the code executes even if you do not print(response)
