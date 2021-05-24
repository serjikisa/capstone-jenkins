# Project hosted on Github Url: https://github.com/serjikisagholian/capstone-jenkins
## Pre Install
- Install aws cli, to communicate with the cloud via command line
- Install python3.6+ if not installed
- Create new virtualenv and activate
```
>> mkdir ~/Envs
>> python3 -m venv ~/Envs/env01
>> source ~/Envs/env01/bin/activate
```
- Install ansible
```
>> pip install ansible
```
- Install boto3
```
>> pip install boto3
```
- Install ansible addons for aws
```
>> ansible-galaxy collection install community.aws
```
- Download and install vagrant for local version from https://www.vagrantup.com/


## Setting credetinals for AWS connection
Before begin set the following environment variables by the following bash commands, replace values <> placeholders with real values

```
>> export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY>
>> export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_KEY>
>> export AWS_SECURITY_TOKEN=<AWS_SECURITY_TOKEN>
>> export AWS_REGION=<AWS_REGION>
```

## Provision AWS resources
The aws_provision.yml playbook will create all resources needed on aws.

- Will create keypair and download it on local
- Will create EC2 group with proper inbound, outbound rules (allowing on port 8080, 22, 5000)
- Will create 1 EC2 instance as master, and will create and asssing Elastic IPs to it.
- Will add created nodes to ansible_hosts file and also known_hosts
```
>> ansible-playbook aws_provision.yml
```

## Test AWS connectivity
```
>> ssh -i ~/.aws/my_keypair.pem ubuntu@<ip-address>
OR
>> ansible -m ping master -i ansible_hosts

```

## Install JVM, Jenkins and Maven
```
# AWS
>> ansible-playbook install.yml -i ansible_hosts
# Vagrant
>> vagrant up  # for the first will create vm and will run ansible playbook
>> vagrant provision   # if VM already created
```

## Setup Jenkins
- Browse Jenkins http://<server-ip-address>:8080
- ssh into server 
```
>> ssh -i ~/.aws/my_keypair.pem ubuntu@<ip-address>
# OR Vagrant version:
>> vagrant ssh
```
- Get administrator token to unlock
```
>> sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
- Copy & pasten token in Jenkins page and follow next steps

## Create an Run Jenkins pipeline
- Create a Jenkins new Item
- Select pipeline, name it and save
- On configuration page, goto: Adavanced options ->  Pipeline (Definition)
- Select Pipeline script from SCM
- Select Git for SCM and specify your repo url (https://github.com/serjik1024/simplepy)
- Save and Run Build

## Run application
### On Server
- browse http://192.168.60.10:8080/  (for vagrant)
- for aws get the server IP from ansible_hosts file
- The applicaiton will simply return 'OK'

### Locally
```
>> git clone https://github.com/serjik1024/simplepy
>> cd simplepy
>> pytest -v   # Run tests
>> python main.py
>> curl localhost:5000
```

### On Docker locally
```
>> cd simplepy
>> docker build . -t simpleapp
>> docker run simplepy pytest -v   # run tests
>> docker run -p 5000:5000 -d --name=simplepy_instance simplepy
>> curl localhost:5000
```