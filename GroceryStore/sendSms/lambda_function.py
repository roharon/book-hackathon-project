import os
import logging
import boto3

DATABASE_NAME = "grocery_store"
GROUPS_COLLECTION_NAME = "groups"
CONNECTION_STRING = os.environ.get("DOCUMENT_DB_CONNECTION_STRING")


def lambda_handler(event, context):
    try:
        phone_number = event["phone_number"]
        sender = event["sender"]
        message = event["message"]

        client = boto3.client("sns")

        response = client.publish(
            PhoneNumber=phone_number,
            Message=message,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': sender
                },
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'
                }
            }
        )

        logging.info("Message ist sent to %s with MessageId %s",
                     event["phone_number"], response['MessageId'])

    except Exception as e:
        logging.error(e)
