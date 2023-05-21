import awswrangler as wr
import os
from datetime import datetime


def lambda_handler(event, context):
    """Converts csv to parquet and creates glue catalog data table.
    We get the s3 bucket name and the object key from event, and set the
    Glue catalog db_name and table_name based on the path of the object that
    was uploaded."""

    # Get the source bucket and object name as passed to the Lambda function
    bucket = event["bucket"]
    key = event["key"]

    # Set the Glue Catalog DB and table name based on the last two elements
    # of the path prior to the file name.
    key_list = key.split("/")
    print(f"key_list: {key_list}")
    db_name = key_list[len(key_list) - 1].split(".")[0]
    print(f"db_name: {db_name}")
    table_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"table_name: {table_name}")

    # print out some debug type information that will be captured in our
    # lambda function logs.
    print(f"Bucket: {bucket}")
    print(f"key: {key}")

    input_path = f"s3://{bucket}/{key}"
    print(f"Input_Path: {input_path}")
    output_path = f"s3://{os.environ['clean_zone_bucket_name']}/{db_name}/{table_name}"
    print(f"Output_Path: {output_path}")

    # read the contents of the CSV file into a pandas DataFrame we
    input_df = wr.s3.read_excel(input_path, sheet_name=None)
    db_names_list = []
    for df_sheet in input_df:
        db_name = db_name + "_" + str(df_sheet)
        current_databases = wr.catalog.databases()
        # wr.catalog.databases()
        if db_name not in current_databases.values:
            print(f"- Database {db_name} does not exist... creating")
            wr.catalog.create_database(db_name)
        else:
            print(f"- Database {db_name} already exists.")

        # use the AWS Data Wrangler library to create a Parquet file
        print("starting save to parquet")

        result = wr.s3.to_parquet(
            df=input_df,
            path=output_path,
            dataset=True,
            database=db_name,
            table=table_name,
            mode="append",
        )
        db_names_list.append(db_name)
    payload = {"db_name": db_names_list}
    return payload
