# aws-data-lakehouse
An AWS Data Lakehouse for analytics on Lisbon AirBnB data


## Setup 

1. Create stack using cloudformation.yml
2. Configure Lambda trigger
    - This is challenging to do in cloudformation as it creates circular dependencies
    - solution is to create trigger in the console after stack creation
3. Load data to landing zone using cli command: ``` aws s3 cp <local_filepath> s3://<bucket_name>/<key>```
Note:
 - added 'AWSLambdaBasicExecutionRole' policy to 'AirbnbS3GlueLambdaRole' Role



## Useful AWS CLI Commands

#### Copy local data to s3 bucket
 - ```aws s3 cp <local_filepath> s3://<bucket_name>/<key>```
 - i.e : ```aws s3 cp listings.csv s3://lg-airbnb-staging-data-landing-zone/listings/data_from_2023-03-19/listings.csv```

#### Delete a file from an s3 bucket
 -  ```aws s3api delete-object --bucket <bucket_name> --key <key>```
 -  i.e: ```aws s3api delete-object --bucket lg-airbnb-staging-data-landing-zone --key testdb/csvparquet/test.csv```




 