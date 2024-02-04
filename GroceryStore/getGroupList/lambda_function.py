import os
import json
from bson.objectid import ObjectId

import pymongo

DATABASE_NAME = "grocery_store"
GROUPS_COLLECTION_NAME = "groups"
CONNECTION_STRING = os.environ.get("DOCUMENT_DB_CONNECTION_STRING")


def lambda_handler(event, context):
    collection = mongo_client()[GROUPS_COLLECTION_NAME]

    participation_conditions = [{"place": "이마트 ABC점"}, {"place": "홈플러스 XYZ점"}]  # TODO: 유저의 참여조건을 불러오다.
    cursor = collection.find({"participation_conditions": {"$in": participation_conditions}})

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


def mongo_client():
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]

    return db
