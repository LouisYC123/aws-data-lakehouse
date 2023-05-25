import boto3
import json
import os


def lambda_handler(event, context):
    """Creates a Redshift 'external' schema using Glue Catalog database"""

    redshift_data_client = boto3.client("redshift-data")
    sql = f"""
            create external schema {event['filename']} 
            from data catalog database '{event['filename']}'
            iam_role '{os.environ['redshift_role_arn']}'  
            create external database if not exists;
        """
    response = redshift_data_client.execute_statement(
        ClusterIdentifier=os.environ["cluster_id"],
        Database=os.environ["redshift_db_name"],
        Sql=sql,
        SecretArn=os.environ["secret_arn"],
    )
    return json.dumps(response, default=str)
