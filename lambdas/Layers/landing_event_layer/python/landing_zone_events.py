import awswrangler as wr
import os
from datetime import datetime
from typing import Dict


def get_source_event_info(bucket: str, key: str) -> dict:
    """Gets the EventBridge event info regarding the file
    uploaded to the Landing Zone"""
    key_list = key.split("/")
    filename = key_list[len(key_list) - 1]
    print(f"filename: {filename}")
    upload_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"upload_date: {upload_date}")
    return {
        'bucket': bucket,
        'key': key,
        'filename': filename,
        'upload_date': upload_date,
    }


def create_source_target_s3_keys(source_info: Dict[str, str]) -> Dict[str, str]:
    '''Creates input_path and output_path s3_keys using source event info'''
    return {
        'input_path': f"s3://{source_info['bucket']}/{source_info['key']}",
        'output_path': f"s3://{os.environ['clean_zone_bucket_name']}/{source_info['filename']}/{source_info['upload_date']}"
    }


def create_glue_tables(source_info: Dict[str, str]):
    """Creates Glue database for the uploaded file"""
    current_databases = wr.catalog.databases()
    db_name = source_info['filename']
    if db_name not in current_databases.values:
        print(f"- Database {db_name} does not exist... creating")
        wr.catalog.create_database(db_name)
    else:
        print(f"- Nothing to do: Database {db_name} already exists.")


def convert_csv_to_parquet(source_info: Dict[str, str], s3_paths: Dict[str, str]) -> Dict[str, str]:
    """Reads the target csv file into a Dataframe, then saves as a parquet file
    in the target s3 output_path and updates the Glue Catalog."""
    # read the contents of the CSV file into a pandas DataFrame
    input_df = wr.s3.read_csv(s3_paths['input_path'])
    print(f"df shape: {str(input_df.shape)}")
    # use the AWS Data Wrangler library to create a Parquet file
    result = wr.s3.to_parquet(
        df=input_df,
        path=s3_paths['output_path'],
        dataset=True,
        database=source_info['filename'],
        table=source_info['upload_date'],
        mode="append",
    )
    return {
        "db_name": source_info['filename'],
        "source_bucket": source_info['bucket'],
        "source_s3_key": source_info['key'],
    }


def convert_excel_to_parquet(source_info: Dict[str, str], s3_paths: Dict[str, str]) -> Dict[str, str]:
    """Reads the target excel file into a Dataframe, then saves as a parquet file
    in the target s3 output_path and updates the Glue Catalog."""
    # read the contents of the CSV file into a pandas DataFrame
    input_df = wr.s3.read_excel(s3_paths['input_path'])
    for df_sheet in input_df:
        db_name = source_info['filename'] + "_" + str(df_sheet)
        current_databases = wr.catalog.databases()
        if db_name not in current_databases.values:
            print(f"- Database {db_name} does not exist... creating")
            wr.catalog.create_database(db_name)
        else:
            print(f"- Database {db_name} already exists.")
        print(f"df shape: {str(input_df.shape)}")
        # use the AWS Data Wrangler library to create a Parquet file
        result = wr.s3.to_parquet(
            df=input_df,
            path=s3_paths['output_path'],
            dataset=True,
            database=source_info['filename'],
            table=source_info['upload_date'],
            mode="append",
        )
        return {
            "db_name": source_info['filename'],
            "source_bucket": source_info['bucket'],
            "source_s3_key": source_info['key'],
        }
