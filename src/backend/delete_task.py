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
    
    # Get the taskId from the event (assuming it comes as part of pathParameters)
    try:
        task_id = event['pathParameters']['taskId']
    except (TypeError, KeyError) as e:
        logger.error(f"Error extracting taskId from event: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Missing or invalid taskId'})
        }
    
    # Delete the item from the table
    try:
        response = table.delete_item(
            Key={'taskId': task_id},
            ConditionExpression="attribute_exists(taskId)"
        )
        
        # Log the response for debugging
        logger.info(f"Delete response: {response}")

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({'message': f'Task with taskId {task_id} successfully deleted'})
        }
    except boto3.exceptions.Boto3Error as e:
        logger.error(f"DynamoDB error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error deleting task from DynamoDB'})
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Unexpected error occurred'})
        }