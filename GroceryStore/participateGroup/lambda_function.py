import os
from bson.objectid import ObjectId

import pymongo

DATABASE_NAME = "grocery_store"
GROUPS_COLLECTION_NAME = "groups"
CONNECTION_STRING = os.environ.get("DOCUMENT_DB_CONNECTION_STRING")


def lambda_handler(event, context):
    group_id = event['pathParameters']['id']
    email = event["requestContext"]["authorizer"]["email"]

    collection = mongo_client()[GROUPS_COLLECTION_NAME]
    result = collection.update_one({"_id": ObjectId(group_id)}, {"$addToSet": {"members": [email]}})

    return result


def mongo_client():
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]

    return db
