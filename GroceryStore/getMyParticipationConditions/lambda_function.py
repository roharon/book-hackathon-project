import os
import json

import pymongo

DATABASE_NAME = "grocery_store"
PARTICIPATION_CONDITIONS_COLLECTION_NAME = "participation_conditions"
CONNECTION_STRING = os.environ.get("DOCUMENT_DB_CONNECTION_STRING")


def lambda_handler(event, context):
    collection = mongo_client()[PARTICIPATION_CONDITIONS_COLLECTION_NAME]
    collection_result = collection.find_one({"email": event["requestContext"]["authorizer"]["email"]})

    if collection_result is None:
        return {
            "statusCode": 404
        }

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "participation_conditions": collection_result["participation_conditions"]
            }
        )
    }


def mongo_client():
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]

    return db
