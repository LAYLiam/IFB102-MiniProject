# [Bucket]
"""
    Main purpose:
        Handle write requirements to Cloudflare R2 bucket.
    
    [1] <Source used to access R2 in Python via AWS boto3.>
    Cloudflare. (n.d.). Configure boto3 for R2. 
            Retrieved 20 May, 2024 from https://developers.cloudflare.com/r2/examples/aws/boto3/
    [2] <Source used to learn how to upload files to bucket.>
    Amazon Web Services. (n.d.). Uploading files [Boto3 1.34.108 documentation]. 
            Retrieved 20 May, 2024 from https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    [3] <Show to publically access files in the bucket for Twilio API.>
    Cloudflare. (n.d). Create public buckets on R2.
            Retrieved 20 May, 2024 from https://developers.cloudflare.com/r2/buckets/public-buckets/#managed-public-buckets-through-r2dev
"""

import boto3
import sys
import env

"""Write image file to R2 instance.
"""
class s3:
    @staticmethod
    def upload_image(image_path):
        """Upload local image to bucket.
        
        :param image_path: System path to target image.
        :return: null
        """
        s3 = boto3.resource('s3',
            endpoint_url=env.S3_BUCKET_ENDPOINT,
            aws_access_key_id=env.S3_ACCESS_KEY_ID,
            aws_secret_access_key=env.S3_SECRET_ACCESS_KEY)
        s3.meta.client.upload_file(image_path, "Detection", 'detection.png')
        return 
