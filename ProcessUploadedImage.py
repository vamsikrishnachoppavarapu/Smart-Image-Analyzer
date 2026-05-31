import json
import boto3

rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ImageLabels')  # ✅ Make sure this matches exactly

def lambda_handler(event, context):
    print("🔁 Received event:", json.dumps(event))

    for record in event['Records']:
        try:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            print(f"📥 Image uploaded: {bucket}/{key}")

            # 🔍 Call Rekognition
            rekog_response = rekognition.detect_labels(
                Image={'S3Object': {'Bucket': bucket, 'Name': key}},
                MaxLabels=10,
                MinConfidence=75
            )

            labels = [label['Name'] for label in rekog_response['Labels']]
            print(f"🎯 Labels detected: {labels}")

            # 💾 Save to DynamoDB
            db_response = table.put_item(
                Item={
                    'filename': key,
                    'labels': labels
                }
            )
            print("✅ Successfully stored in DynamoDB:", db_response)

        except Exception as e:
            print("❌ ERROR:", str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('Done')
    }
