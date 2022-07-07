
                
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Onramp_events')

# Read the JSON file
with open('clientrecord.json') as json_data:
    items = json.load(json_data)
    print(items)
    with table.batch_writer() as batch:

        # Loop through the JSON objects
        # for item in items:
            batch.put_item(items['awsid'])