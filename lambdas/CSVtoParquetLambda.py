import boto3
import awswrangler as wr
from urllib.parse import unquote_plus

"""This function is called when the Lambda function is executed. The event 
data contains information such as the s3 object that was uploaded and was
the cause of the trigger that ran this function. From this event data, we get
the s3 bucket name and the object key. We also set the Glue catalog db_name
and table_name based on the path of the object that was uploaded."""


def lambda_handler(event, context):
    # Get the source bucket and object name as passed to the Lambda function
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

    # We will set the DB and table name based on the last two elements of the
    # path prior to the file name. If key = 'dms/sakila/film/LOAD01.csv, then the
    # following lines will set db to sakila and table_name to 'film'

    key_list = key.split("/")
    print(f"key_list: {key_list}")
    db_name = key_list[len(key_list) - 3]
    table_name = key_list[len(key_list) - 2]
    file_name = key_list[len(key_list) - 1]

    """We now print out some debug type information that will be captured in our
    lambda function logs. This includes information such as the Amazon s3 bucket
    and key that we are processing. We then set the output_path value here, which
    is where we are going to write the Parquet file that this function creates.
    """

    print(f"Bucket: {bucket}")
    print(f"key: {key}")
    print(f"DB Name: {db_name}")
    print(f"Table Name: {table_name}")
    print(f"Filename: {file_name}")

    input_path = f"s3://{bucket}/{key}"
    print(f"Input_Path: {input_path}")
    output_path = f"s3://lg-airbnb-staging-data-clean-zone/{db_name}/{table_name}"
    print(f"Output_Path: {output_path}")

    """We can then use the AWS Data Wrangler library to read the CSV file that 
    we received. We read the contents of the CSV file into a pandas DataFrame we
    are calling input_df. We also get a list of current Glue databases, and if the
    database we want to use does not exist, we create it."""

    input_df = wr.s3.read_csv(input_path)
    print(f"df shape: {str(input_df.shape)}")
    current_databases = wr.catalog.databases()
    wr.catalog.databases()
    if db_name not in current_databases.values:
        print(f"- Database {db_name} does not exist... creating")
        wr.catalog.create_database(db_name)
    else:
        print(f"- Database {db_name} already exists.")

    """Finally, we can use the AWS Data Wrangler library to create a Parquet file
    containing the data we read from the CSV file. For the S3 to Parquet function,
    we specify the name of the dataframe (input_df) that contains the data we want
    to write out in Parquet format. We also specify the S3 output path, the Glue
    Database, and the table name."""
    print("starting save to parquet")

    result = wr.s3.to_parquet(
        df=input_df,
        path=output_path,
        dataset=True,
        database=db_name,
        table=table_name,
        mode="append",
    )

    print("RESULT: ")
    print(f"{result}")

    return result
