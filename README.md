UBUNTU setup 

sudo apt-get update     /    sudo yum update
sudo apt-get -y upgrade / sudo yum -y upgrade

sudo apt-get install -y python3-pip / sudo yum install -y python3-pip
sudo apt install python3 python3-venv / sudo yum install python3 python3-venv

mkdir ~/.venv
python3 -m venv ~/.venv
source .venv/bin/activate          |      / deactivate


//creating a vertual env another method
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
virtualenv myvenv 
source myvenv/bin/activate


pip install PyGithub
pip3 install boto3
pip install GitPython

pip install slackclient slackeventsapi Flask
pip3 install boto3
pip3 install slack_bolt


export SLACK_APP_TOKEN=
export SLACK_BOT_TOKEN=
export SLACK_SIGNING_SECRET=
-------------------------------------------------------
create s3 bucket onrampbot
Create a DDB table 'rampbot' and partition key 'awsid'

run 'python3 ./app/main.py' 

------------ECS setup----------------------------------
#create requirements.txt file
source ~/.venvs/slackbot/bin/activate
pip freeze > requirements.txt   

#create dockerfile 
        FROM python:3.8
        WORKDIR /bolt-app
        COPY requirements.txt .
        RUN pip install -r requirements.txt
        COPY ./app ./app
        CMD ["python", "./app/main.py"]


#follow push command for ECR 



aws ecs delete-cluster --cluster slack-interface      


----------------------Create slack app-----------------------------
display_information:
  name: OnRampBot
features:
  bot_user:
    display_name: OnRampBot
    always_online: false
  shortcuts:
    - name: Onramp request
      type: global
      callback_id: onramp
      description: aws lambda requests
  slash_commands:
    - command: /add
      description: Insert the client deatils
      should_escape: false
oauth_config:
  scopes:
    bot:
      - channels:history
      - chat:write
      - groups:history
      - im:history
      - mpim:history
      - incoming-webhook
      - commands
settings:
  event_subscriptions:
    bot_events:
      - message.channels
      - message.groups
      - message.im
      - message.mpim
  interactivity:
    is_enabled: true
  org_deploy_enabled: false
  socket_mode_enabled: true
  token_rotation_enabled: false


****make sure Socket Mode enable 
get following env 

