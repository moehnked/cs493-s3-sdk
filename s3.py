import boto3
import logging
import sys
from botocore.exceptions import ClientError

#use: python s3.py <bucket> <filepath to upload>

if len(sys.argv) < 3:
    print "use: python s3.py <bucket> <filepath to upload>"
    sys.exit("please use proper arguments")

sess = boto3.Session(profile_name='s3advisor')
s3_client = sess.client('s3')
s3_resource = sess.resource('s3')

def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def create_bucket(bucket_name):
    try:
        s3_client.create_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True



response = s3_client.list_buckets()

foundMatchingBucket = False
#find the bucket to upload into
for bucket in response['Buckets']:
    if bucket["Name"] == sys.argv[1]:
        print "match!"
        foundMatchingBucket = True
        #upload file into bucket
        upload_file(sys.argv[2], bucket["Name"])

if not foundMatchingBucket:
    print "no match found, creating new bucket"
    create_bucket(sys.argv[1])
    upload_file(sys.argv[2], bucket["Name"])
    

