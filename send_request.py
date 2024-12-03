import json
import boto3
import os

# Initialize the SQS client
sqs_client = boto3.client('sqs', region_name='us-east-1')


class WidgetRequestHandler:
    def __init__(self, sqs_client):
        # Retrieve the queue URL from environment variables
        self.queue_url = os.environ.get('QUEUE_URL')
        if not self.queue_url:
            raise ValueError("QUEUE_URL environment variable is not set.")
        self.sqs_client = sqs_client

    def validate_request(self, request_data):
        """
        Validate the widget request.
        The request must include:
        - A valid 'type' field with values 'create', 'update', or 'delete'.
        - A valid 'widgetId' field.
        """
        available_requests = ['create', 'update', 'delete']

        if 'type' not in request_data or request_data['type'] not in available_requests:
            raise ValueError("Invalid request type. Must be 'create', 'update', or 'delete'.")

        if 'widgetId' not in request_data:
            raise ValueError("WidgetId is required.")

        return True

    def add_to_sqs_queue(self, widget_request):
        """
        Add the widget request to the SQS queue.
        """
        message_body = json.dumps(widget_request)
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
            self.validate_request(request_data)
            response = self.add_to_sqs_queue(request_data)

            return {
                "status": "success",
                "message": "Request successfully added to the queue.",
                "MessageId": response['MessageId']
            }
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e)
            }
        except Exception as e:
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

        http_method = event.get('httpMethod', None)
        print(http_method)
        print(event)

        if event.get('body'):
            widget_data = json.loads(event['body'])  # Parse the string into a dictionary
        else:
            widget_data = {}

        # Initialize the WidgetRequestHandler
        widget_handler = WidgetRequestHandler(sqs_client)

        # Process the widget request
        result = widget_handler.process_widget_request(widget_data)

        # Return the result back to the API Gateway
        return {
            "statusCode": 200 if result['status'] == 'success' else 400,
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": str(e)})
        }
