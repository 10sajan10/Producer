import json
import boto3

# Initialize the SQS client
sqs_client = boto3.client('sqs', region_name='us-east-1')
queue_url = 'https://sqs.us-east-1.amazonaws.com/186579595491/cs5250-requests'

def add_to_sqs_queue(widget_request, sqs_client, queue_url):
    """
    Add a widget request to an AWS SQS queue.

    Args:
    widget_request (dict): The widget request data to send to the queue.
    """
    # Convert the widget request dictionary to a JSON string
    message_body = json.dumps(widget_request)

    # Send the message to the SQS queue
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )

    # Print response (including MessageId)
    print(f"Message added to SQS queue: {response['MessageId']}")

def widget_request_handler(request_data):
    """
    Simulates the Lambda function handling the incoming API Gateway request.
    This function processes the incoming request and places it in a queue.
    """
    # Extract data from the request
    Available_request = ['create', 'update', 'delete']
    if request_data.get('type') in Available_request:
        widget_request = request_data

        # Add the processed widget request to the queue
        add_to_sqs_queue(widget_request, sqs_client, queue_url)

        return {"status": "success", "message": "Request added to queue."}
    else:
        print("Request Invalid")
        return {"status": "error", "message": "Invalid request type."}

def lambda_handler(event, context):
    """
    The entry point for the Lambda function that handles the API Gateway event.
    """
    try:
        # Parse the incoming event body as JSON
        widget_data = json.loads(event['body'])

        # Handle the widget request
        result = widget_request_handler(widget_data)

        # Return the result back to the API Gateway
        return {
            "statusCode": 200 if result['status'] == 'success' else 400,
            "body": json.dumps(result)
        }

    except Exception as e:
        # Handle any errors
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": str(e)})
        }
