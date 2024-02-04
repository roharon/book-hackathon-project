import os
import json
from bson.objectid import ObjectId

import pymongo

DATABASE_NAME = "grocery_store"
GROUPS_COLLECTION_NAME = "groups"
PARTICIPATION_CONDITIONS_COLLECTION_NAME = "participation_conditions"
CONNECTION_STRING = os.environ.get("DOCUMENT_DB_CONNECTION_STRING")


def lambda_handler(event, context):
    groups_collection = mongo_client()[GROUPS_COLLECTION_NAME]

    participation_conditions = get_participation_conditions(event["requestContext"]["authorizer"]["email"])
    cursor = groups_collection.find({"participation_conditions": {"$in": participation_conditions}})

    groups = []

    for group in cursor:
        groups.append(
            {
                "id": str(group["_id"]),
                "name": group["group_name"],
                "participation_conditions": group["participation_conditions"]
            }
        )

    return {
        "statusCode": 200,
        "body": json.dumps(
            groups
        )
    }


def get_participation_conditions(email):
    collection = mongo_client()[PARTICIPATION_CONDITIONS_COLLECTION_NAME]
    collection_result = collection.find_one({"email": email})

    return collection_result["participation_conditions"] if collection_result is not None else []


def mongo_client():
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]

    return db
