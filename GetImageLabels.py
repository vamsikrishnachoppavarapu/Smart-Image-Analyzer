import json
import boto3
import traceback

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'ImageLabels'  # ✅ Make sure it exactly matches your table
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print("📥 Incoming event:", json.dumps(event))

    try:
        # Check for query string parameter
        if "queryStringParameters" not in event or event["queryStringParameters"] is None:
            print("❌ Missing queryStringParameters in request.")
            return {
                "statusCode": 400,
                "headers": { "Access-Control-Allow-Origin": "*" },
                "body": json.dumps({"error": "Missing queryStringParameters"})
            }

        filename = event["queryStringParameters"].get("filename") or event["queryStringParameters"].get("imageKey")

        if not filename:
            print("❌ 'filename' parameter is missing.")
            return {
                "statusCode": 400,
                "headers": { "Access-Control-Allow-Origin": "*" },
                "body": json.dumps({"error": "Missing 'filename' query parameter"})
            }

        print(f"🎯 Querying DynamoDB for filename: {filename}")

        # Query DynamoDB
        response = table.get_item(Key={'filename': filename})

        if 'Item' in response:
            print(f"✅ Found item: {response['Item']}")
            return {
                "statusCode": 200,
                "headers": { "Access-Control-Allow-Origin": "*" },
                "body": json.dumps(response['Item'])
            }
        else:
            print(f"⚠️ No labels found for: {filename}")
            return {
                "statusCode": 404,
                "headers": { "Access-Control-Allow-Origin": "*" },
                "body": json.dumps({"message": f"No labels found for {filename}."})
            }

    except Exception as e:
        # Log stack trace to CloudWatch
        print("❌ Exception occurred while querying DynamoDB.")
        traceback.print_exc()

        return {
            "statusCode": 500,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": json.dumps({
                "error": "Internal Server Error",
                "message": str(e)
            })
        }
