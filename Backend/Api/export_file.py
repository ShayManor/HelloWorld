import boto3

s3_client = boto3.client('s3')
bucket_name = 'manors-videos-bucket'
file_path = 'final_movie.mp4'
object_name = 'video.mp4'  # Name to store the file in S3

# Upload the file
s3_client.upload_file(file_path, bucket_name, object_name)
