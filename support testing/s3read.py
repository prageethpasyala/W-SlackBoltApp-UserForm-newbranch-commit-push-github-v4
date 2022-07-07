

import json
import boto3




s3 = boto3.client('s3')
bucket = 'onramp-client-lzn-terraform-tfvarfies'
key = 'clientrecord.json'

response = s3.get_object(Bucket = bucket, Key = key)
content = response['Body']
jsonObject = json.loads(content.read())

print(jsonObject)