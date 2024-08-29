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
    
    # Validate and extract taskId from pathParameters
    try:
        task_id = event['pathParameters']['taskId']
    except (TypeError, KeyError) as e:
        logger.error(f"Error extracting taskId: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Missing or invalid taskId'})
        }
    
    # Parse request body
    try:
        body = json.loads(event['body'])
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing request body: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid JSON in request body'})
        }
    
    # Initialize update expression and values
    update_expression = "SET "
    expression_attribute_values = {}
    expression_attribute_names = {}

    # Build the update expression
    if 'title' in body:
        update_expression += "#title = :title, "
        expression_attribute_values[':title'] = body['title']
        expression_attribute_names['#title'] = "title"
    
    if 'status' in body:
        update_expression += "#status = :status, "
        expression_attribute_values[':status'] = body['status']
        expression_attribute_names['#status'] = "status"
    
    if 'description' in body:
        update_expression += "#description = :description, "
        expression_attribute_values[':description'] = body['description']
        expression_attribute_names['#description'] = "description"
    
    # Remove the trailing comma and space from the expression
    update_expression = update_expression.rstrip(", ")
    
    # Perform the item update
    try:
        response = table.update_item(
            Key={'taskId': task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ConditionExpression="attribute_exists(taskId)"
        )

        # Get the complete task after the update
        response = table.get_item(Key={'taskId': task_id})
        
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps(response['Item'])
        }
    except boto3.exceptions.Boto3Error as e:
        logger.error(f"DynamoDB error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error updating task in DynamoDB'})
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Unexpected error occurred'})
        }