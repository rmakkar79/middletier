import whois
import datetime
import os
import json
import requests

def lambda_handler(event, context):
    AlertExpirationDays = os.environ["AlertExpirationDays"]
    urls = os.environ["urls"]
    slackRestEndpoint = os.environ["slackRestEndpoint"]
    checkDomainExpiration(urls,AlertExpirationDays,slackRestEndpoint)

def checkDomainExpiration(urls,AlertExpirationDays,slackRestEndpiont):
    for url in urls.split(","):
        print ("checking for %s" %url)
        w = whois.whois(url)
        stringExpiration=(str(w["expiration_date"])[:10])
        stringNow=str(datetime.datetime.utcnow())[:10]
        stringDateExp=datetime.datetime.strptime(stringExpiration,'%Y-%m-%d')
        stringDateNow= datetime.datetime.strptime(stringNow,'%Y-%m-%d')
        daytoexprire=stringDateExp-stringDateNow
        if daytoexprire.days > int(AlertExpirationDays):
            print (daytoexprire.days)
        else:
            sendNotificationSlack(slackRestEndpiont, "Domain going to expire: " + url)
            print ("Domain going to expire")

def sendNotificationSlack(slackRestEndpiont,slackMessage):
    headers={'Content-type': 'application/json'}
    respone = requests.post(slackRestEndpiont,data=json.dumps({"text": slackMessage}), headers=headers)

lambda_handler("eve","con")




