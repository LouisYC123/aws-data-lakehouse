import boto3

def get_client(resource: str):
    """Returns a boto3 connection client for given resource, e.g - S3"""
    return boto3.client(resource)


def get_session_resource(resource: str):
    """Returns a boto3 connection resource for given service, e.g - S3"""
    return boto3.Session().resource(resource)


def delete_s3_object(
    s3_resource: boto3.client,
    bucket_name: str,
    s3_key: str
    ) -> None:
    """Deletes an S3 object"""
    return s3_resource.Object(bucket_name, s3_key).delete()


def create_copy_source(
    source_bucket_name: str,
    source_key: str
    )-> dict:
    """Creates a copy_source dict containing source bucket name and source
    key name to be used in copy_s3_object()."""
    return {
        'Bucket': source_bucket_name,
        'Key': source_key,
    }


def copy_s3_object( 
    s3_resource: boto3.client,
    copy_source: dict,
    target_bucket_name: str,
    target_key: str,
    ) -> dict:
    """Copies an S3 object from source to target S3 locations"""
    return s3_resource.meta.client.copy(copy_source, target_bucket_name,target_key)


def archive_client_files(
    source_bucket_name: str,
    source_key: str,
    target_bucket_name: str,
    target_key: str
    ):
    """Archives client files that have been succesfully imported by
    moving them from the drop-zone subfolder to the archived subfolder
    """
    s3_resource = get_session_resource('s3')
    # Copy object to the _archived folder
    copy_s3_object(
        s3_resource=s3_resource,
        copy_source=create_copy_source(source_bucket_name, source_key),
        target_bucket_name=target_bucket_name,
        target_key=target_key,
    )
    # Delete object from the "drop-zone"
    delete_s3_object(
        s3_resource=s3_resource,
        bucket_name=source_bucket_name,
        s3_key=source_key,
    )
