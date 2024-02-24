import json
import boto3
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')
sqs = boto3.client('sqs')


def upload_image(event, context):
    bucket_name = 'your-bucket-name'
    image_key = event['filename']  # Assuming the filename is sent in the request

    # Save the image to S3 bucket
    s3.put_object(Bucket=bucket_name, Key=image_key, Body=event['image'])

    # Enqueue a message to SQS for thumbnail generation
    queue_url = 'your-sqs-queue-url'
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps({'bucket': bucket_name, 'key': image_key}))

    return {
        'statusCode': 200,
        'body': json.dumps('Image uploaded successfully.')
    }


def generate_thumbnail(event, context):
    records = event['Records']
    for record in records:
        message = json.loads(record['body'])
        bucket_name = message['bucket']
        image_key = message['key']

        # Fetch the image from S3
        response = s3.get_object(Bucket=bucket_name, Key=image_key)
        image_data = response['Body'].read()

        # Generate thumbnail
        img = Image.open(BytesIO(image_data))
        img.thumbnail((100, 100))
        thumbnail_key = f"thumbnails/{image_key}"  # Assuming thumbnails are stored in a directory called 'thumbnails'

        # Save thumbnail to S3
        with BytesIO() as output:
            img.save(output, format='JPEG')
            thumbnail_data = output.getvalue()
            s3.put_object(Bucket=bucket_name, Key=thumbnail_key, Body=thumbnail_data)

    return {
        'statusCode': 200,
        'body': json.dumps('Thumbnail generated successfully.')
    }


def download_image(event, context):
    bucket_name = 'your-bucket-name'
    image_key = event['filename']  # Assuming the filename is sent in the request

    # Get the image from S3
    response = s3.get_object(Bucket=bucket_name, Key=image_key)
    image_data = response['Body'].read()

    return {
        'statusCode': 200,
        'body': image_data,
        'headers': {
            'Content-Type': 'image/jpeg'
        }
    }


def download_thumbnail(event, context):
    bucket_name = 'your-bucket-name'
    image_key = f"thumbnails/{event['filename']}"  # Assuming thumbnails are stored in a directory called 'thumbnails'

    # Get the thumbnail from S3
    response = s3.get_object(Bucket=bucket_name, Key=image_key)
    thumbnail_data = response['Body'].read()

    return {
        'statusCode': 200,
        'body': thumbnail_data,
        'headers': {
            'Content-Type': 'image/jpeg'
        }
    }
