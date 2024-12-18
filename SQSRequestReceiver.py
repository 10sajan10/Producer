import boto3
import botocore
import logging

class SQSRequestReceiver:

    def __init__(self, url):
        self.sqs_client = boto3.client('sqs', region_name='us-east-1')
        self.url = url

    def retrieve_messages_from_queue(self,maxno=20):
        try:
            response = self.sqs_client.receive_message(
            QueueUrl=self.url,
            MaxNumberOfMessages=maxno,
            VisibilityTimeout=600,
            WaitTimeSeconds=20
        )
            messages = response.get('Messages', None)
            if not messages:
                print("No messages")
                exit()
            else:
                for message in messages:
                    print(message)
                    print("\n")

            return messages
        except botocore.exceptions.ClientError as e:
            logging.error("Something went wrong")
            logging.error(e)
            exit()


SQSRequestReceiver(url='https://sqs.us-east-1.amazonaws.com/186579595491/cs5250-requests').retrieve_messages_from_queue(maxno=10)