import logging
import json
from cgitb import text
from distutils.command.clean import clean
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import boto3
from botocore.exceptions import NoCredentialsError

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Step 5: Payload is sent to this endpoint, we extract the `trigger_id` and call views.open
@app.command("/add")
def handle_command(body, ack, client, logger):
    logger.info(body)
    ack()

    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "gratitude-modal",
            "title": {"type": "plain_text", "text": "Landing Zone App"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "my_block_0",
                    "element": {"type": "plain_text_input", "action_id": "comp_name", "placeholder": {"type":  "plain_text","text": "company name"}},
                    "label": {"type": "plain_text", "text": "Company Name"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_1",
                    "element": {"type": "plain_text_input", "action_id": "email", "placeholder": {"type":  "plain_text","text": "your-email@domain.com"}},
                    "label": {"type": "plain_text", "text": "E-mail Address"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_2",
                    "element": {"type": "plain_text_input", "action_id": "awsaccnum", "placeholder": {"type":  "plain_text","text": "7367799xxxxx"}},
                    "label": {"type": "plain_text", "text": "AWS-Account Number"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_3",
                    "element": {"type": "plain_text_input", "action_id": "extid", "placeholder": {"type":  "plain_text","text": "cloudreach-(single word)"}},
                    "label": {"type": "plain_text", "text": "External ID"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_4",
                    "element": {"type": "plain_text_input", "action_id": "cidr", "placeholder": {"type":  "plain_text","text": "10.0.0.0/16"}},
                    "label": {"type": "plain_text", "text": "CIDR Block"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_5",
                    "element": {"type": "plain_text_input", "action_id": "whitelist", "placeholder": {"type":  "plain_text","text": "10.0.1.0/24-(Optional)"}},
                    "label": {"type": "plain_text", "text": "Whitelist"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_6",
                    "element": {"type": "plain_text_input", "action_id": "vpcname", "placeholder": {"type":  "plain_text","text": "CR_VPC_Main"}},
                    "label": {"type": "plain_text", "text": "VPC Name"},
                },
                {
			"type": "input",
			"block_id": "my_block_8",
			"element": {
				"type": "static_select",
				"action_id": "static_select-action",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a Region"
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "eu-west-1"
						},
						"value": "eu-west-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "eu-west-2"
						},
						"value": "eu-west-2"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "us-west-1"
						},
						"value": "us-west-1"
					}
				]
			},
			"label": {
				"type": "plain_text",
				"text": "Label"
			}
		}
                ],
        },
    )
    logger.info(res)

    
    
# Step 4: The path that allows for your server to receive information from the modal sent in Slack
@app.view("gratitude-modal")
def view_submission(ack, body, client, logger, say):
    ack()
        
    logger.info(body["view"]["state"]["values"])
    # Extra Credit: Uncomment out this section
    cloudreach_client_records = "C03AGA96W87"
    user_text_0 = body["view"]["state"]["values"]["my_block_0"]["comp_name"]["value"]
    user_text_1 = body["view"]["state"]["values"]["my_block_1"]["email"]["value"]
    user_text_2 = body["view"]["state"]["values"]["my_block_2"]["awsaccnum"]["value"]
    user_text_3 = body["view"]["state"]["values"]["my_block_3"]["extid"]["value"]
    user_text_4 = body["view"]["state"]["values"]["my_block_4"]["cidr"]["value"]
    user_text_5 = body["view"]["state"]["values"]["my_block_5"]["whitelist"]["value"]
    user_text_6 = body["view"]["state"]["values"]["my_block_6"]["vpcname"]["value"]
    user_text_7 = body["view"]["state"]["values"]["my_block_8"]["static_select-action"]["selected_option"]["value"]
    client.chat_postMessage(channel=cloudreach_client_records, text="|------------------------ New record -------------------------|")
    client.chat_postMessage(channel=cloudreach_client_records, text="Company Name : "+user_text_0)
    client.chat_postMessage(channel=cloudreach_client_records, text="Email Address : "+user_text_1)
    client.chat_postMessage(channel=cloudreach_client_records, text="AWS Account Number : "+user_text_2)
    client.chat_postMessage(channel=cloudreach_client_records, text="External ID : "+user_text_3)
    client.chat_postMessage(channel=cloudreach_client_records, text="CIDR Block : "+user_text_4)
    client.chat_postMessage(channel=cloudreach_client_records, text="Whitelist subnet : "+user_text_5)
    client.chat_postMessage(channel=cloudreach_client_records, text="VPC Name : "+user_text_6)
    client.chat_postMessage(channel=cloudreach_client_records, text="Region : "+user_text_7)
    # client.chat_postMessage(channel=cloudreach_client_records, text="!!! SUCCESSFULLY RECORDED !!! ")
    say("*<fakeLink.toUserProfiles.com|Please re-check entered values : >*",channel="C03AGA96W87")
    say(
        blocks=[
                {
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*Click to continue*"
				},
				"accessory": {
					"type": "button",
					"action_id": "button_click_4",
					"text": {
						"type": "plain_text",
						# "emoji": true,
						"text": "Continue"
					},
					"value": "click_me_123"
				}
			},
            {
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*Click to Cancel*"
				},
				"accessory": {
					"type": "button",
					"action_id": "button_click_5",
					"text": {
						"type": "plain_text",
						# "emoji": true,
						"text": "Cancel"
					},
					"value": "click_me_123"
				}
			}
        ],channel="C03AGA96W87"
    )
# ---------------terraform dump------------------
    f= open("terraform.tfvars","w+")
        
    f.write('comp_name = "'+ str(user_text_0)+'"\n')
    f.write('email = "'+ str(user_text_1)+'"\n')
    f.write('awsaccnum = "'+ str(user_text_2)+'"\n')
    f.write('extid = "'+ str(user_text_3)+'"\n')
    f.write('cidr = "'+ str(user_text_4)+'"\n')
    f.write('whitelist = "'+ str(user_text_5)+'"\n')
    f.write('vpcname = "'+ str(user_text_6)+'"\n')
    f.write('region = "'+ str(user_text_7)+'"\n')
    
    f.close()
# -------create a new folder with client id num in S3 and upload the tfvars file -----
    #  it has to be encoded to do this
    string = "dfghj"
    encoded_string = string.encode("utf-8")

    bucket_name = "onramp-client-lzn-terraform-tfvarfies"
    file_name = "terraform.tfvars"
    s3_path = str(user_text_2) + "/" + file_name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)

# -------json dump-----------------------------
    cl_details = [{
    'id' : user_text_2,
    'comp_name': user_text_0,
    'email': user_text_1, 
    
    'extid' : user_text_3,
    'cidr' : user_text_4,
    'whitelist' : user_text_5,
    'vpcname' : user_text_6,
    'region' : user_text_7
    
    }]
    # awsid = user_text_2
    # comp_name = user_text_0
    # action_button_click(ack,say, awsid, comp_name)
    with open('clientrecord.json', 'w') as json_file:
        json.dump(cl_details, json_file)

    upload_to_aws('clientrecord.json', 'onramp-client-lzn-terraform-tfvarfies', 'clientrecord.json')
    
    

# ----------------json file uploading to s3 root--------------------------
def upload_to_aws(local_file, bucket, s3_file):
    # s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
    #                 aws_secret_access_key=SECRET_KEY)
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

uploaded = upload_to_aws('clientrecord.json', 'onramp-client-lzn-terraform-tfvarfies', 'clientrecord.json')

# ---------------------------button click continue/save to ddb-------------------------

@app.action("button_click_4")
def action_button_click(ack, say ):
    ack()
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    table = dynamodb.Table('Onramp_events')
    with open("clientrecord.json") as json_file:
        Items = json.load(json_file)
    # Sneakers = json.load(json_file)
        for item in Items:
            awsid = item['id']
            comp_name = item['comp_name']
            email = item['email']
            extid = item['extid']
            cidr = item['cidr']
            whitelist = item['whitelist']
            vpcname = item['vpcname']
            region = item['region']
            print("Adding sneaker:", awsid, comp_name,email, extid,extid,cidr,whitelist,vpcname,region)

            table.put_item(
            Item={
                'awsid': awsid,
                'comp_name': comp_name,
                'comp_name': comp_name,
                'email': email,
                'extid': extid,
                'extid': extid,
                'cidr': cidr,
                'whitelist': whitelist,
                'vpcname': vpcname,
                'region': region
            }
        )
    say("Entry added successfully to the DDB!!")
    









# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


    # https://slack.dev/bolt-python/tutorial/getting-started
            # run followign command to activate the virtual env
                #   python3 -m venv .venv
                #   source .venv/bin/activate

    # type @boltpython hello