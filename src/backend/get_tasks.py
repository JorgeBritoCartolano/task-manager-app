import json
import boto3
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
    
    try:
        # Scan the table to get all items
        response = table.scan()
            
        # Get the items from the response
        tasks = response.get('Items', [])
        logger.info(f"Retrieved {len(tasks)} tasks")
            
        # Return a successful response with the list of tasks
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({
                'tasks': tasks
            })
        }
    except boto3.exceptions.Boto3Error as e:
        logger.error(f"DynamoDB error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error retrieving tasks from DynamoDB'})
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Unexpected error occurred'})
        }