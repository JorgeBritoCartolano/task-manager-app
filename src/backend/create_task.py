import json
import boto3
import uuid
import logging
import os

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Get table name from environment variable
    table_name = os.environ['TABLE_NAME']
    
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Decode the request body
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Error parsing request body'})
        }
    
    # Validate required fields
    required_fields = ['title', 'status', 'description']
    missing_fields = [field for field in required_fields if field not in body]
    
    if missing_fields:
        logger.warning(f"Missing fields: {', '.join(missing_fields)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Missing required fields: {", ".join(missing_fields)}'})
        }
    
    # Generate a unique taskId
    task_id = str(uuid.uuid4())
    
    # Create the task object
    new_task = {
        'taskId': task_id,
        'title': body['title'],
        'status': body['status'],
        'description': body['description']
    }
    
    # Save the task in DynamoDB
    try:
        table.put_item(Item=new_task)
        logger.info(f"Task created successfully: {new_task}")
        
        return {
            'statusCode': 201,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps(new_task)
        }
    except boto3.exceptions.Boto3Error as e:
        logger.error(f"DynamoDB error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error saving task to DynamoDB'})
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Unexpected error occurred'})
        }