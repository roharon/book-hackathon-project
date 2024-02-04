import os
import json

import pymongo

DATABASE_NAME = "grocery_store"
PARTICIPATION_CONDITIONS_COLLECTION_NAME = "participation_conditions"
CONNECTION_STRING = os.environ.get("DOCUMENT_DB_CONNECTION_STRING")


def lambda_handler(event, context):
    body = json.loads(event["body"])
    participation_conditions = body["participation_conditions"]

    email = event["requestContext"]["authorizer"]["email"]
    collection = mongo_client()[PARTICIPATION_CONDITIONS_COLLECTION_NAME]

    collection.update_one({"email": email},
                          {"$set": {"participation_conditions": participation_conditions}},
                          upsert=True)

    return {
        "statusCode": 201,
        "body": json.dumps(
            {
                "participation_conditions": participation_conditions
            }
        )
    }


def mongo_client():
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]

    return db
