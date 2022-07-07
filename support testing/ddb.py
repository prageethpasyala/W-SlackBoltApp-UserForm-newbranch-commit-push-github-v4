import boto3
import random
from decimal import *
def load_transactions(dynamodb,t1):
    table = dynamodb.Table('Onramp_events')
    trans = {}
    trans['awsid'] = "sd1"
    trans['amount'] = str(t1)
    trans['transDate'] = '2020-03-19'
    print(trans)
    table.put_item(Item=trans)
if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb',region_name='eu-west-2')
    t1="test34"
    load_transactions(dynamodb,t1)