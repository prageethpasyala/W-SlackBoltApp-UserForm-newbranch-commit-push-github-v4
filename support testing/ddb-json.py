import boto3
import json
access_key="AKIASZAXXD4DOTEQWFRS"
secret_access_key="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"
session=boto3.Session(aws_access_key_id=access_key,aws_secret_access_key=secret_access_key, region_name='eu-west-2')
client_dynamo=session.resource('dynamodb')
table=client_dynamo.Table('Onramp_events')

records=""
with open('clientrecord.json','r') as datafile:
  records=json.load(datafile)
print(records['email'])

count=0;
for i in records:
    print(records[i])
    i['awsid']={records['id']}
#   print(i)
#   i['comp_name']=i['comp_name']
#   i['email']=i['email']
    table.put_item(Item=i)
#   count+=1
