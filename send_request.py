import json
import boto3

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
    Available_request = ['create','update','delete']
    if request_data.get('type') in Available_request:
        widget_request = request_data

    else:
        print("request Invalid")

    # Add the processed widget request to the queue
    add_to_queue(widget_request)

    # Return a response (simulating Lambda response)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Widget request submitted successfully'})}


file_path = r'sample-requests/1612306368338'

# Open and read the file
with open(file_path, 'r') as file:
    file_content = file.read()

# Parse the content as a JSON dictionary
widget_data = json.loads(file_content)

# Print the dictionary
print(widget_data)