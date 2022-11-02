from http import client
import logging
import json
from cgitb import text
from distutils.command.clean import clean
import os
from slack_bolt import App, response
from slack_bolt.adapter.socket_mode import SocketModeHandler
import boto3
from botocore.exceptions import NoCredentialsError
import datetime , time
from random import randint
import requests

client = boto3.client('ssm',region_name='us-east-1')
responseAppToken = client.get_parameter(Name='SLACK_APP_TOKEN')
responseBotToken = client.get_parameter(Name='SLACK_BOT_TOKEN')
apptoken=responseAppToken['Parameter']['Value']
bottoken=responseBotToken['Parameter']['Value']

app = App(token=bottoken)
# app = App(token=responseBotToken)


# Step 5: Payload is sent to this endpoint, we extract the `trigger_id` and call views.open
@app.command("/new")
def handle_command(body, ack, client, logger):
    logger.info(body)
    ack()

    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "gratitude-modal",
            "title": {"type": "plain_text", "text": "Landing Zone Form"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "my_block_0",
                    "element": {"type": "plain_text_input", "action_id": "comp_name", "placeholder": {"type":  "plain_text","text": "No special characters, no spaces, lower case"}},
                    "label": {"type": "plain_text", "text": "Company Name"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_1",
                    "element": {"type": "plain_text_input", "action_id": "email", "placeholder": {"type":  "plain_text","text": "All lowercase"}},
                    "label": {"type": "plain_text", "text": "E-mail Address"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_2",
                    "element": {"type": "plain_text_input", "action_id": "awsaccnum", "placeholder": {"type":  "plain_text","text": "Enter 12 digit account number"}},
                    "label": {"type": "plain_text", "text": "SheardService Account Number"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_3",
                    "element": {"type": "plain_text_input", "action_id": "extid", "placeholder": {"type":  "plain_text","text": "No special characters, no spaces"}},
                    "label": {"type": "plain_text", "text": "External ID"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_4",
                    "element": {"type": "plain_text_input", "action_id": "cidr", "placeholder": {"type":  "plain_text","text": "Enter VPC cidr  eg. 10.0.0.0/16"}},
                    "label": {"type": "plain_text", "text": "CIDR Block"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_5",
                    "element": {"type": "plain_text_input", "action_id": "whitelist", "placeholder": {"type":  "plain_text","text": "Enter multiple cidr with comma seperated (Optional)"}},
                    "label": {"type": "plain_text", "text": "Whitelist CIDR"},
                },
                {
                    "type": "input",
                    "block_id": "my_block_6",
                    "element": {"type": "plain_text_input", "action_id": "vpcname", "placeholder": {"type":  "plain_text","text": "Enter vpc name - no spaces"}},
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
							"text": "eu-west-3"
						},
						"value": "eu-west-3"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "us-west-1"
						},
						"value": "us-west-1"
					},
                    {
						"text": {
							"type": "plain_text",
							"text": "us-west-2"
						},
						"value": "us-west-2"
					},
                    {
						"text": {
							"type": "plain_text",
							"text": "us-east-1"
						},
						"value": "us-east-1"
					},
                    {
						"text": {
							"type": "plain_text",
							"text": "us-east-2"
						},
						"value": "us-east-2"
					}
				]
			},
			"label": {
				"type": "plain_text",
				"text": "Region"
			}
		},
        {
            "type": "input",
            "block_id": "my_block_9",
            "element": {"type": "plain_text_input", "action_id": "env", "placeholder": {"type":  "plain_text","text": "Eg: dev, prod ( No special characters, no spaces )"}},
            "label": {"type": "plain_text", "text": "Env"},
                },
        {
            "type": "input",
            "block_id": "my_block_10",
            "element": {"type": "plain_text_input", "action_id": "gwip", "placeholder": {"type":  "plain_text","text": "Enter ip address without subnet eg 10.0.1.1 "}},
            "label": {"type": "plain_text", "text": "Customer Gateway"},
                },
        {
            "type": "input",
            "block_id": "my_block_11",
            "element": {"type": "plain_text_input", "action_id": "aft", "placeholder": {"type":  "plain_text","text": "Enter 12 digit account number"}},
            "label": {"type": "plain_text", "text": "AFT Account Number"},
                },
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
    slackbot_onramp = "C041ZAP38CQ"
    
    user_text_0 = body["view"]["state"]["values"]["my_block_0"]["comp_name"]["value"]
    user_text_1 = body["view"]["state"]["values"]["my_block_1"]["email"]["value"]
    user_text_2 = body["view"]["state"]["values"]["my_block_2"]["awsaccnum"]["value"]
    user_text_3 = body["view"]["state"]["values"]["my_block_3"]["extid"]["value"]
    user_text_4 = body["view"]["state"]["values"]["my_block_4"]["cidr"]["value"]
    user_text_5 = body["view"]["state"]["values"]["my_block_5"]["whitelist"]["value"]
    user_text_6 = body["view"]["state"]["values"]["my_block_6"]["vpcname"]["value"]
    user_text_8 = body["view"]["state"]["values"]["my_block_8"]["static_select-action"]["selected_option"]["value"]
    user_text_9 = body["view"]["state"]["values"]["my_block_9"]["env"]["value"]
    user_text_10 = body["view"]["state"]["values"]["my_block_10"]["gwip"]["value"]
    user_text_11= body["view"]["state"]["values"]["my_block_11"]["aft"]["value"]
    client.chat_postMessage(channel=slackbot_onramp, text="----------: Entered details :--------------")
    client.chat_postMessage(channel=slackbot_onramp, text="- Company Name : "+user_text_0.lower())
    client.chat_postMessage(channel=slackbot_onramp, text="- Email Address : "+user_text_1)
    client.chat_postMessage(channel=slackbot_onramp, text="- SharedService Acc Num : "+user_text_2)
    client.chat_postMessage(channel=slackbot_onramp, text="- External ID : "+user_text_3)
    client.chat_postMessage(channel=slackbot_onramp, text="- CIDR Block : "+user_text_4)
    client.chat_postMessage(channel=slackbot_onramp, text="- Whitelist CIDR : "+user_text_5)
    client.chat_postMessage(channel=slackbot_onramp, text="- VPC Name : "+user_text_6)
    client.chat_postMessage(channel=slackbot_onramp, text="- Region : "+user_text_8)
    client.chat_postMessage(channel=slackbot_onramp, text="- Env : "+user_text_9)
    client.chat_postMessage(channel=slackbot_onramp, text="- Gateway : "+user_text_10)
    client.chat_postMessage(channel=slackbot_onramp, text="- AFT Acc Num : "+user_text_11)
    client.chat_postMessage(channel=slackbot_onramp, text="--------------------------------------------")
    # form input conditions 
    # import string
    import re
    regex = re.compile('[0-9,.]+.')
    regex1 = re.compile('[0-9,.]+.')
    regex2 = re.compile('[0-9,.]+.')

    

    if len(user_text_2) != 12 and user_text_2.isnumeric() != True:
        say(":warning: *Input ERROR* : Account SharedService Acc number must be 12 digit or all numeric. Please run '/new' command to re-try.",channel="C041ZAP38CQ")
    elif re.search("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", user_text_1) == None:
        say(":warning: *Input ERROR* : check your email format. Please run '/new' command to re-try.",channel="C041ZAP38CQ")
    elif regex.match(user_text_4)==None:
        say(":warning: *Input ERROR* : check your cidr format. Please run '/new' command to re-try.",channel="C041ZAP38CQ")
    elif regex1.match(user_text_5)==None:
        say(":warning: *Input ERROR* : check your WhiteList cidr format. Please run '/new' command to re-try.",channel="C041ZAP38CQ")
    elif regex2.match(user_text_10)==None:
        say(":warning: *Input ERROR* : check your GateWay address format. Please run '/new' command to re-try",channel="C041ZAP38CQ")
    elif len(user_text_11) != 12 :
        say(":warning: *Input ERROR* : Account AFT Acc number must be 12 digit. Please run '/new' command to re-try.",channel="C041ZAP38CQ")


     
   
    else:
        
        say(":bell: *Verify your inputs :* ",channel="C041ZAP38CQ")
        say(
            blocks=[
                    {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Click for Continue"
                    },
                    "accessory": {
                        "type": "button",
                        "action_id": "button_click_44",
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
                        "text": "Click for Cancel"
                    },
                    "accessory": {
                        "type": "button",
                        "action_id": "button_click_55",
                        "text": {
                            "type": "plain_text",
                            # "emoji": true,
                            "text": "Cancel"
                        },
                        "value": "click_me_123"
                    }
                }
            ],channel="C041ZAP38CQ"
        )
    

    
    view_submission.var0 = str(user_text_0).lower()
    view_submission.var1 = str(user_text_1)
    view_submission.var2 = str(user_text_2)
    view_submission.var3 = str(user_text_3)
    view_submission.var4 = str(user_text_4)
    view_submission.var5 = str(user_text_5)
    view_submission.var6 = str(user_text_6)
    view_submission.var8 = str(user_text_8)
    view_submission.var9 = str(user_text_9)
    view_submission.var10 = str(user_text_10)
    view_submission.var11 = str(user_text_11)

    
    
# # ---------------------------button click continue/save to ddb-------------------------

@app.action("button_click_44")
def action_button_click(ack, say):
    ack()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('serverlessrepo-onramp-form-FormDataTable-13NPSDX8KPSY3')
    user_text_0 = view_submission.var0
    user_text_1 = view_submission.var1
    user_text_2 = view_submission.var2
    user_text_3 = view_submission.var3
    user_text_4 = view_submission.var4
    user_text_5 = view_submission.var5
    user_text_6 = view_submission.var6
    user_text_8 = view_submission.var8
    user_text_9 = view_submission.var9
    user_text_10 = view_submission.var10
    user_text_11 = view_submission.var11

    ts = time.time()
    created = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')   

    n=7
    range_start = 10**(n-1)
    range_end = (10**n)-1
    formId=randint(range_start, range_end)

    itemLitList='{"customername":"'+str(user_text_0)+'", "email" : "'+str(user_text_1)+'", "AccountNumber":"'+str(user_text_2)+'", "ext_id":"'+str(user_text_3)+'", "cidr":"'+str(user_text_4)+'", "Whitelist":"'+str(user_text_5)+'", "vpcname":"'+str(user_text_6)+'", "region":"'+str(user_text_8)+'", "env":"'+str(user_text_9)+'", "cgwIP":"'+str(user_text_10)+'", "aft_acct":"'+str(user_text_11)+'" }'
    table.put_item(Item={'formId' : str(formId) , 'created':str(created), 'formData' : itemLitList  } ) 

    # table.put_item(Item={'awsid':str(user_text_11),'comp_name':str(user_text_0), 'email' : str(user_text_1), 'sharedacc':str(user_text_2), 'extid':str(user_text_3), 'cidr':str(user_text_4), 'wlist':str(user_text_5), 'vpcname':str(user_text_6), 'region':str(user_text_8), 'env':str(user_text_9), 'gw':str(user_text_10), 'aft':str(user_text_11)})
    
    say(":white_check_mark: Completed \n \n *Thank you for filling out your information!* \n We will look over your details and get back to you soon. \n _OnRamp Team_ \n :smile: Cheers!")

    URL = f"https://5nbdz8lkog.execute-api.us-east-1.amazonaws.com/v1/id?id="
    headers = {"Contenet-Type": "yourstage/yourpath"}
    r = requests.request("GET", URL, headers=headers)
    say(":busts_in_silhouette: Sent ECS task restart request.",channel="C041ZAP38CQ")
    
@app.action("button_click_55")
def action_button_click(ack, say ):
    ack() 
    say(":exclamation: *Entered values have been deleted. Please fill it again.* \n:bulb: Type  '/new'  to start")





# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, apptoken).start()
    # SocketModeHandler(app, responseAppToken).start()