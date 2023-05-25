import os
import s3_interactions


def lambda_handler(
    event, 
    context,
    ):
    """Archives client files that have been succesfully imported by
    moving them from the drop-zone subfolder to the archived subfolder
    """
    source_bucket = os.environ['landing_zone_bucket_name']
    target_bucket = os.environ['archive_zone_bucket_name']
    s3_interactions.archive_client_files(
        source_bucket_name=source_bucket,
        source_key=event['source_key'],
        target_bucket_name=target_bucket,
        target_key=event['filename'],
        )

