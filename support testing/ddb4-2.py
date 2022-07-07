import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
table = dynamodb.Table('Sneakers')
with open("app/sneakerdata.json") as json_file:
    Sneakers = json.load(json_file)
    # Sneakers = json.load(json_file)
    for sneaker in Sneakers:
        brand = sneaker['brand']
        model = sneaker['model']

        print("Adding sneaker:", brand, model)

        table.put_item(
           Item={
               'brand': brand,
               'model': model,
            }
        )

        # https://towardsaws.com/how-to-create-an-aws-dynamodb-table-using-python-scripts-and-aws-cloud-9-ide-33a1d1fa0441