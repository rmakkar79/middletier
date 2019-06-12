# middletier
Stuff related to middle tier like web/app server

1. sslCertCheck

This is a lambda which can be used in AWS public cloud. 
Settings for lambda :
- Runtime : 3.7
- Handler : lambdaCheckSsslExpiration.lambda_handler
- Environment variables:
    - AlertExpirationDays
