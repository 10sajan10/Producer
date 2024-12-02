import json
import boto3

# Initialize the SQS client
sqs_client = boto3.client('sqs', region_name='us-east-1')
queue_url = 'https://sqs.us-east-1.amazonaws.com/186579595491/cs5250-requests'

# Helper class to handle widget requests
class WidgetRequestHandler:
    def __init__(self, sqs_client, queue_url):
        self.sqs_client = sqs_client
        self.queue_url = queue_url

    def validate_request(self, request_data):
        """
        Validate the widget request.
        The request must include a valid 'type' field with values 'create', 'update', or 'delete'.
        """
        available_requests = ['create', 'update', 'delete']
        if 'type' not in request_data or request_data['type'] not in available_requests:
            raise ValueError("Invalid request type. Must be 'create', 'update', or 'delete'.")
        return True

    def add_to_sqs_queue(self, widget_request):
        """
        Add the widget request to the SQS queue.
        """
        # Convert the widget request dictionary to a JSON string
        message_body = json.dumps(widget_request)

        # Send the message to the SQS queue
        response = self.sqs_client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message_body
        )

        return response

    def process_widget_request(self, request_data):
        """
        Main processing function for widget requests. This includes validation and adding to the queue.
        """
        try:
            # Validate the widget request
            self.validate_request(request_data)

            # Add the request to the SQS queue
            response = self.add_to_sqs_queue(request_data)

            return {
                "status": "success",
                "message": "Request successfully added to the queue.",
                "MessageId": response['MessageId']
            }

        except ValueError as e:
            # Handle invalid request type
            return {
                "status": "error",
                "message": str(e)
            }
        except Exception as e:
            # Handle general errors
            return {
                "status": "error",
                "message": "An error occurred while processing the request.",
                "error": str(e)
            }

# Lambda handler function (entry point)
def lambda_handler(event, context):
    """
    The entry point for the Lambda function that handles the API Gateway event.
    """
    try:
        # Parse the incoming event body as JSON
        widget_data = json.loads(event['body'])

        # Initialize the WidgetRequestHandler
        widget_handler = WidgetRequestHandler(sqs_client, queue_url)

        # Process the widget request
        result = widget_handler.process_widget_request(widget_data)

        # Return the result back to the API Gateway
        return {
            "statusCode": 200 if result['status'] == 'success' else 400,
            "body": json.dumps(result)
        }

    except Exception as e:
        # Handle any errors in the Lambda function
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": str(e)})
        }
