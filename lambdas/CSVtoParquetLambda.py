from landing_zone_events import (
    get_source_event_info,
    create_source_target_s3_keys,
    create_glue_tables,
    convert_csv_to_parquet,
)


def lambda_handler(event, context):
    """Converts csv to parquet and creates glue catalog data table.
    We get the s3 bucket name and the object key from event, and set the
    Glue catalog db_name and table_name based on the path of the object that
    was uploaded."""
    source_event_info = get_source_event_info(
        bucket=event["source_bucket"],
        key=event["source_key"],
        )
    s3_paths = create_source_target_s3_keys(source_event_info)
    create_glue_tables(source_event_info)
    convert_csv_to_parquet(source_event_info, s3_paths)
    return {
        'db_name': event['filename'],
        'source_s3_key': s3_paths['input_path'],
        }


