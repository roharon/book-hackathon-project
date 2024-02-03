import os
import json
from bson.objectid import ObjectId

import pymongo

DATABASE_NAME = "grocery_store"
GROUPS_COLLECTION_NAME = "groups"
CONNECTION_STRING = os.environ.get("DOCUMENT_DB_CONNECTION_STRING")


def lambda_handler(event, context):
    group_id = event['pathParameters']['id']
    current_user_email = event["requestContext"]["authorizer"]["email"]

    db_client = mongo_client()[GROUPS_COLLECTION_NAME]
    group = db_client.find_one({"_id": ObjectId(group_id)})

    if group is None:
        return {
            "statusCode": 404
        }

    if group["owner_email"] != current_user_email:
        return {
            "statusCode": 403
        }

    db_client.delete_one({"_id": ObjectId(group_id)})

    return {
        "statusCode": 204
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
