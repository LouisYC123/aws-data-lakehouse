# aws-data-lakehouse
An AWS Data Lakehouse for analytics on Lisbon AirBnB data

![lisbon-datalake_V3 drawio](https://github.com/LouisYC123/aws-data-lakehouse/assets/97873724/5955bb96-6613-41d0-bf19-24ad21ccf02c)


## Setup 
1. Create bucket for lambdas and upload lambda zips
2. add your email to Secrets Manager, this will be used for notification alerts. Add the secret's arn to line XXX (~302, in MySecretEmailAttachment:Properties:SecretId )
1. Create stack using cloudformation.yml
3. Load data to landing zone using cli command: ``` aws s3 cp <local_filepath> s3://<bucket_name>/<key>```
4. Query data with AWS Athena and identify 'hot' data to be loaded to warehouse
Note:
 - added 'AWSLambdaBasicExecutionRole' and 'AmazonRedshiftFullAccess' and 'SecretsManagerReadWrite' policy to 'AirbnbS3GlueLambdaRole' Role


 - Define external table
## Governance & Security


## Useful AWS CLI Commands
** TODO - add more here for setting up AWS CLI
- ```aws configure```  

- Load local data to s3 bucket
    - ```aws s3 cp <local_filepath> s3://<bucket_name>/<key>```
    - i.e : ```aws s3 cp test.csv s3://lg-airbnb-staging-data-landing-zone/test.csv```

- Delete a file from an s3 bucket
 -  ```aws s3api delete-object --bucket <bucket_name> --key <key>```
 -  i.e: ```aws s3api delete-object --bucket lg-airbnb-staging-data-landing-zone --key testdb/csvparquet/test.csv```

- zip a file
    - ```zip -r Layers/boto3_layer.zip Layers/boto3_layer```



![lisbon-airbnb-steps drawio](https://github.com/LouisYC123/aws-data-lakehouse/assets/97873724/7cb03522-2106-4d9b-8bef-9b6618dc56fb)

![lisbon-airbnb-steps drawio](https://github.com/LouisYC123/aws-data-lakehouse/assets/97873724/7cb03522-2106-4d9b-8bef-9b6618dc56fb)

