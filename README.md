# aws-data-lakehouse
An AWS Data Lakehouse for analytics on Lisbon AirBnB data


## Setup 

1. Create stack using cloudformation.yml
2. Configure Lambda trigger
    - This is challenging to do in cloudformation as it creates circular dependencies
    - solution is to create trigger in the console after stack creation:
        First, you will need to grant permission for the S3 bucket to invoke the Lambda function using the aws lambda add-permission command:
        ```
            aws lambda add-permission \
            --function-name <MyFunction> \
            --action "lambda:InvokeFunction" \
            --principal s3.amazonaws.com \
            --source-arn arn:aws:s3:::<MyBucket> \
            --statement-id s3-trigger
        ```
    - Next, you can use the aws s3api put-bucket-notification-configuration command to set up the S3 trigger:
    ```
            aws s3api put-bucket-notification-configuration \
            --bucket my-bucket \
            --notification-configuration '{
                "LambdaFunctionConfigurations": [
                {
                    "LambdaFunctionArn": "<MyLambdaFunctionArn>",
                    "Events": ["s3:ObjectCreated:*"],
                    "Filter": {
                    "Key": {
                        "FilterRules": [
                        {
                            "Name": "suffix",
                            "Value": ".csv"
                        }
                        ]
                    }
                    }
                }
                ]
            }'

    ```

3. Load data to landing zone using cli command: ``` aws s3 cp <local_filepath> s3://<bucket_name>/<key>```
Note:
 - added 'AWSLambdaBasicExecutionRole' policy to 'AirbnbS3GlueLambdaRole' Role

## Governance & Security


## Useful AWS CLI Commands

#### Load local data to s3 bucket
 - ```aws s3 cp <local_filepath> s3://<bucket_name>/<key>```
 - i.e : ```aws s3 cp listings.csv s3://lg-airbnb-staging-data-landing-zone/listings/data_from_2023-03-19/listings.csv```

#### Delete a file from an s3 bucket
 -  ```aws s3api delete-object --bucket <bucket_name> --key <key>```
 -  i.e: ```aws s3api delete-object --bucket lg-airbnb-staging-data-landing-zone --key testdb/csvparquet/test.csv```



![lisbon-airbnb-steps drawio](https://github.com/LouisYC123/aws-data-lakehouse/assets/97873724/7cb03522-2106-4d9b-8bef-9b6618dc56fb)

