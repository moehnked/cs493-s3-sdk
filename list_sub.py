import boto3
import logging
import sys
from botocore.exceptions import ClientError

sess = boto3.Session(profile_name='s3advisor')
s3 = sess.resource('s3')

prefix = "sub/"
bucket = s3.Bucket(name="pyciode-test")
FilesNotFound = True
for obj in bucket.objects.filter(Prefix=prefix):
     print('{0}:{1}'.format(bucket.name, obj.key))
     FilesNotFound = False
if FilesNotFound:
     print("ALERT", "No file in {0}/{1}".format(bucket, prefix))