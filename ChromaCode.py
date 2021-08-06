
import boto3
import sys
from botocore.exceptions import ClientError


def check_aws_validity(key_id, secret):
    try:
        s3 = boto3.client('s3', aws_access_key_id=key_id,
                          aws_secret_access_key=secret)
        response = s3.list_buckets()
        print("response is " + response)
        return True

    except Exception as e:
        if str(e) != "An error occurred (InvalidAccessKeyId) when calling the ListBuckets operation: The AWS Access Key Id you provided does not exist in our records.":
            return True
        return False


def runEncryptionCheck(key_id, secret_key):
    
    if check_aws_validity(key_id, secret_key) == False:
        print(
            'InvalidAccessKeyId, The AWS Access Key Id provided does not exist in records')
        sys.exit()

    s3 = boto3.client('s3', aws_access_key_id=key_id, aws_secret_access_key=secret_key)

    response = s3.list_buckets()

    for bucket in response['Buckets']:
        try:
            enc = s3.get_bucket_encryption(Bucket=bucket['Name'])
            rules = enc['ServerSideEncryptionConfiguration']['Rules']
            print('Bucket: %s, Encryption: %s' % (bucket['Name'], rules))
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                print('Bucket: %s, no server-side encryption' %
                      (bucket['Name']))
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print('Bucket: %s, User already exists' % (bucket['Name']))
            if e.response['Error']['Code'] == 'IllegalLocationConstraintException':
                print('Bucket: %s, Bad location' % (bucket['Name']))
            if e.response['Error']['Code'] == 'InvalidObjectState':
                print('Bucket: %s, Invalid Object Error' % (bucket['Name']))
            #else:
            #    print("Bucket: %s, unexpected error: %s" % (bucket['Name'], e))



runEncryptionCheck("","")
