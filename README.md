# middletier
Stuff related to middle tier like web/app server

1. sslCertCheck

This is a lambda which can be used in AWS public cloud. 
Settings for lambda :
- Runtime : 3.7
- Handler : lambdaCheckSsslExpiration.lambda_handler
- Environment variables:
    - AlertExpirationDays ( example: 10 )
    - slackRestEndpiont ( example: https://hooks.slack.com/services/<something>/<something> )
    - urls ( example: {"www.google.com":"443","www.yahoo.com":"443"} )
 
 Rest everything is default.
 
 You can create a AWS Cloudwatch rule to run on a certain schedule.
