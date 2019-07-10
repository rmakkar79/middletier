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
      *you can have different port for https above.
 
 Rest everything is default.
 
 You can create a AWS Cloudwatch rule to run on a certain schedule.

Now to upload this lambda , you need all the dependencies packed with it following this link https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

In my personal development environment , i have amazon linux docker image (https://hub.docker.com/_/amazonlinux) where i create the package 
so it can be as close as possible to the lambda run time environment.

In case you dont want to do that work , i have the zip file also in github. Hopefully just uploading it should be fine.

2. checkDomainExpiration

Settings for lambda :
- Runtime : 3.6
- Handler : checkDoaminExpiration.lambda_handler
- Environment variables:
    - AlertExpirationDays ( example: 10 )
    - slackRestEndpiont ( example: https://hooks.slack.com/services/<something>/<something> )
    - urls ( example: google.com,yahoo.com )
       
 Rest everything is default.
 
 You can create a AWS Cloudwatch rule to run on a certain schedule.


