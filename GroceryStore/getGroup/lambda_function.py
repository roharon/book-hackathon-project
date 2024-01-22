import os
import json

import pymongo

DATABASE_NAME = "grocery_store"
GROUPS_COLLECTION_NAME = "groups"
CONNECTION_STRING = os.environ.get("DOCUMENT_DB_CONNECTION_STRING")


def lambda_handler(event, context):
    group_id = event['pathParameters']['id']

    db_client = mongo_client()[GROUPS_COLLECTION_NAME]
    result = db_client.find_one({"_id": group_id})

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "id": result["_id"],
                "name": result["group_name"],
                "participation_conditions": result["participation_conditions"]
            }
        )
    }


def bad_reqeust(message):
    return {
        "statusCode": 400,
        "body": json.dumps({
            "message": message
        })
    }


def mongo_client():
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]

    return db
