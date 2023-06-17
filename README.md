# aws-data-lakehouse
** *WIP* **  
This repo contains a cloudformation template to build a Data LakeHouse on AWS for Lisbon Property Data

![lisbon-datalake_V3 drawio](https://github.com/LouisYC123/aws-data-lakehouse/assets/97873724/c6dc32de-02e8-4a7b-861a-5f9a877c7b13)



The CloudFormation template will create a stack incorporating the core features required for the Data LakeHouse on AWS including:
- S3 Landing zone
- S3 Clean zone
- S3 Archive Zone
- EventBrige Rules to trigger StepFunctions State Machine when new file arrives in landing zone
- Logging configuration
- Redshift Clusters
- SNS email notifications for arrival of new data, State Machine success and State Machine failure
- Python Lambdas for data processing
- Lambda Layers for code deployment
- Secrets manager for Redshift credentials access and rotation
- All neccessary IAM roles


Complete Data Lakehouse will hold:
 - Lisbon AirBnb data downloaded from insideairbnb.com  (In Progress)
 - Lisbon property data scraped from www.Idealista.pt (ToDo)
 - Lisbon property data scraped from www.green-acres.pt (ToDo)
 - Lisbon property data scraped from www.rebrealty.com (ToDo)


## How to use 
1. Create bucket for lambdas and upload lambda zips in ```/lambdas/```
2. Add your email to Secrets Manager, this will be used for notification alerts.
1. Create stack using cloudformation.yml
3. Load data to landing zone using cli command: ``` aws s3 cp <local_filepath> s3://<bucket_name>/<key>```



## Governance & Security

**TODO**

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
