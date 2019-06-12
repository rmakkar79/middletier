import OpenSSL
import ssl,socket
import datetime
import requests
import json
import os

def lambda_handler(event, context):
    AlertExpirationDays=os.environ["AlertExpirationDays"]
    urls=json.loads(os.environ["urls"])
    slackRestEndpiont=os.environ["slackRestEndpiont"]
    checkSSLlife(urls,AlertExpirationDays,slackRestEndpiont)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def checkSSLlife(urls,AlertExpirationDays,slackRestEndpiont):
    currentDT=datetime.datetime.now()
    currentTime=[int(currentDT.year),int(currentDT.month),int(currentDT.day)]
    for url,port in urls.items():
        print ("checking for %s" % url)
        cert=ssl.get_server_certificate((url,port))
        x509=OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,cert)
        yearMonDay=str(x509.get_notAfter())[:10][-8:]
        expirationTime=[int(yearMonDay[:4]),int(yearMonDay[-4:-2]),int(yearMonDay[-2:])]
        if expirationTime[0]-currentTime[0] <= 0:
            print ("Year Expired-slack")
            #sendNotificationSlack(slackRestEndpiont,"Sab theek hai -" + url)
            if expirationTime[1]-currentTime[1] <= 0:
                print ("Month Expired")
                if expirationTime[2]-currentTime[2] < AlertExpirationDays:
                    print ("Day Expired")
                    sendNotificationSlack(slackRestEndpiont, "Sab theek hai -" + url)
                    return "Expired"
                else:
                    print ("Day Not Expired")
                    return "ALLGOOD"
            else:
                print ("Month NOT Expired")
                return "ALLGOOD"
        else:
            print ("Year NOT EXPIRED")

def sendNotificationSlack(slackRestEndpiont,slackMessage):
    headers={'Content-type': 'application/json'}
    respone = requests.post(slackRestEndpiont,data=json.dumps({"text": slackMessage}), headers=headers)

#lambda_handler("asdf","asdf")
