import json
import boto3
import cfnresponse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print('Received event: {}'.format(json.dumps(event)))
    
    response_data = {}
    
    try:
        if event['RequestType'] == 'Delete':
            # Remove notification configuration
            bucket_name = event['ResourceProperties']['BucketName']
            s3.put_bucket_notification_configuration(
                Bucket=bucket_name,
                NotificationConfiguration={}
            )
            print('Removed notification configuration from bucket {}'.format(bucket_name))
        elif event['RequestType'] in ['Create', 'Update']:
            # Set notification configuration
            bucket_name = event['ResourceProperties']['BucketName']
            notification_config = event['ResourceProperties']['NotificationConfiguration']
            
            s3.put_bucket_notification_configuration(
                Bucket=bucket_name,
                NotificationConfiguration=notification_config
            )
            print('Set notification configuration for bucket {}'.format(bucket_name))
            
        cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)
    except Exception as e:
        print('Error: {}'.format(e))
        cfnresponse.send(event, context, cfnresponse.FAILED, {'Error': str(e)}) 