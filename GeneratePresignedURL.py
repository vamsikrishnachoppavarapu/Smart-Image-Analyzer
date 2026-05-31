import json
import boto3
import urllib.parse

s3_client = boto3.client('s3')
BUCKET_NAME = 'smart-image-analyzer'  # 🔥 Your actual bucket name

def lambda_handler(event, context):
    params = event.get("queryStringParameters")
    filename = params.get("filename")

    if not filename:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Filename is required"})
        }

    # ✅ Clean and sanitize filename
    filename = urllib.parse.unquote(filename).strip().replace('\n', '').replace('\r', '')

    # ✅ Generate the pre-signed URL
    url = s3_client.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': filename,
            'ContentType': 'image/jpeg'
        },
        ExpiresIn=300  # URL valid for 5 mins
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "uploadURL": url,
            "filename": filename
        }),
        "headers": {
            "Access-Control-Allow-Origin": "*"  # Allow CORS
        }
    }
