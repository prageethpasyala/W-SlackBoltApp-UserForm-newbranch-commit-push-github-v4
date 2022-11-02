import logging
import json
from cgitb import text
from distutils.command.clean import clean
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import boto3
from botocore.exceptions import NoCredentialsError


import boto3
from boto3.dynamodb.conditions import Key, Attr
import base64
from github import Github
from github import InputGitTreeElement
import git
from git import Repo
import requests
import json
import os, zipfile

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
				"text": "Region"
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
    client.chat_postMessage(channel=cloudreach_client_records, text="----------: Entered details :--------------")
    client.chat_postMessage(channel=cloudreach_client_records, text="- Company Name : "+user_text_0)
    client.chat_postMessage(channel=cloudreach_client_records, text="- Email Address : "+user_text_1)
    client.chat_postMessage(channel=cloudreach_client_records, text="- AWS Account Number : "+user_text_2)
    client.chat_postMessage(channel=cloudreach_client_records, text="- External ID : "+user_text_3)
    client.chat_postMessage(channel=cloudreach_client_records, text="- CIDR Block : "+user_text_4)
    client.chat_postMessage(channel=cloudreach_client_records, text="- Whitelist subnet : "+user_text_5)
    client.chat_postMessage(channel=cloudreach_client_records, text="- VPC Name : "+user_text_6)
    client.chat_postMessage(channel=cloudreach_client_records, text="- Region : "+user_text_7)
    client.chat_postMessage(channel=cloudreach_client_records, text="--------------------------------------------")
    say(":bell: *Verify your inputs :* ",channel="C03AGA96W87")
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
					"text": "Click for Cancel"
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
# ---------------write to local ------------------
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

# -----------------Write to S3----------------------------------->
    
    cidr = str(user_text_4)    
    vpcname = str(user_text_6)
    region = str(user_text_7)
    
    string = 'vpc_tags = { \n' +''+'Name = "'+vpcname+'"\n'+''+'}\n'+''+'cidr = "'+cidr+'" \n'+''+ 'vpcname = "'+vpcname+'"\n'+''+ 'region = "'+region+'" \n' 
                
    encoded_string = string.encode("utf-8")
    bucket_name = "onrampbot"
    file_name = "terraform.tfvars"
    s3_path = "clientdata/" + file_name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
# ---------------------------------------------------------
# -------create a new folder with client id num in S3 and upload the tfvars file ----->
    #  it has to be encoded to do this
    string = 'vpc_tags = { \n' +''+'Name = "'+vpcname+'"\n'+''+'}\n'+''+'cidr = "'+cidr+'" \n'+''+ 'vpcname = "'+vpcname+'"\n'+''+ 'region = "'+region+'" \n'     
    encoded_string = string.encode("utf-8")

    bucket_name = "onrampbot"
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

    upload_to_aws('clientrecord.json', 'onrampbot', 'clientrecord.json')
    
    

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

uploaded = upload_to_aws('clientrecord.json', 'onrampbot', 'clientrecord.json')

# ---------------------------button click continue/save to ddb-------------------------

@app.action("button_click_4")
def action_button_click(ack, say ):
    ack()
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    table = dynamodb.Table('rampbot')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('onrampbot') # just Bucket name
    file_name = 'clientrecord.json'      # full file path
    obj = list(bucket.objects.filter(Prefix=file_name))
    if len(obj) > 0:
        print("S3 file Exists")
    

        s3 = boto3.client('s3')
        bucket = 'onrampbot'
        key = 'clientrecord.json'

        response = s3.get_object(Bucket = bucket, Key = key)
        content = response['Body']
        Items = json.loads(content.read())
        print(Items)
        
        for item in Items:
                awsid = item['id']
                comp_name = item['comp_name']
                email = item['email']
                extid = item['extid']
                cidr = item['cidr']
                whitelist = item['whitelist']
                vpcname = item['vpcname']
                region = item['region']
                print("Adding items:", awsid, comp_name,email, extid,extid,cidr,whitelist,vpcname,region)

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
        say(":white_check_mark: DataBase Update \n \n *Thank you for filling out your information!* \n We will look over your details and get back to you soon. \n _OnRamp Team_ \n :smile: Cheers!")


        # --------------------------------Git Action---------------------------------
        # initializing git repo
        g = Github('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')
        repo = g.get_repo("prageethpasyala/Onramp-ClientRepo-Slackapp")

        # calling branch name from ddb accid
        NewBranchName = awsid

        # create a function
        def function1():
            repo = g.get_repo("prageethpasyala/Onramp-ClientRepo-Slackapp")
            all_files = []
            contents = repo.get_contents("")
            # check  file or  DIR 
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    file = file_content
                    all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
                    
            # open the file and read
            s3 = boto3.client('s3')
            data = s3.get_object(Bucket='onrampbot', Key='clientdata/terraform.tfvars')
            content = data['Body'].read()
            print(content)
            # with open('tmp/bot.tf', 'r') as file:
            #     content = file.read()

            # create the prefix name of the file before Upload to github
            git_prefix = 'OnRampBot_TF/'
            git_file = git_prefix + 'orb.tf'

            # push the file into new branch  
            if git_file in all_files:
                contents = repo.get_contents(git_file)
                repo.update_file(contents.path, "committing files", content, contents.sha, branch=NewBranchName)
                print(git_file + ' File UPDATED')
            else:
                repo.create_file(git_file, "committing files", content, branch=NewBranchName)
                print(git_file + ' File CREATED')



        # checking the brnch exsisitng or not
        listAA = str(list(repo.get_branches()))

        if 'Branch(name="'+NewBranchName+'")' in listAA:
            print("Branch exsist.")
            say(":rotating_light: *ERROR : * Github Branch has not created , branch already exsist. please contact admin!!")
            # s3 = boto3.client('s3')
            # data = s3.get_object(Bucket='onrampbot', Key='clientdata/terraform.tfvars')
            # contents = data['Body'].read()
            # print(contents)
            # function1()

        # create a nwe branch, copy the main branch 'branches[0]' to the new branch
        else:
            print("Branch is creating..")
            headers = {'Authorization': "Token " + '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'}
            url = "https://api.github.com/repos/prageethpasyala/Onramp-ClientRepo-Slackapp/git/refs/heads"
            branches = requests.get(url, headers=headers).json()
            branch, sha = branches[0]['ref'], branches[0]['object']['sha']
            res = requests.post('https://api.github.com/repos/prageethpasyala/Onramp-ClientRepo-Slackapp/git/refs', json={
                "ref": "refs/heads/"+NewBranchName,
                "sha": sha
            }, headers=headers)
            print(res.content)
            print("New branch has been created.")

            # replace the newbranch file by calling the function
            function1()
    
    















    else:
        print("S3 file does Not Exists")
        say(":rotating_light: *ERROR : Please type '/add' command to restart*")

    # from subprocess import call
    # call(["python", "main5w.py"])  

@app.action("button_click_5")
def action_button_click(ack, say ):
    ack()
    s3 = boto3.resource("s3")
    obj = s3.Object("onrampbot", "clientrecord.json")
    obj.delete()
    say(":exclamation: *Record Deleted* \n:bulb: Command '/add' to restart")




# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


    # https://slack.dev/bolt-python/tutorial/getting-started
            # run followign command to activate the virtual env
                #   python3 -m venv .venv
                #   source .venv/bin/activate

    # type @boltpython hello