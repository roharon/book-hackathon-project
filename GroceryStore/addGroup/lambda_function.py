import os
import json

import pymongo

DATABASE_NAME = "grocery_store"
GROUPS_COLLECTION_NAME = "groups"
CONNECTION_STRING = os.environ.get("DOCUMENT_DB_CONNECTION_STRING")


def lambda_handler(event, context):
    body = json.loads(event["body"])
    group_name = body["name"]
    participation_conditions = body["participation_conditions"]

    db_client = mongo_client()[GROUPS_COLLECTION_NAME]

    if type(group_name) is not str:
        return bad_reqeust("그룹 이름이 올바르지 않습니다.")

    if type(participation_conditions) is not list:
        return bad_reqeust("참여 조건이 올바르지 않습니다.")

    group = {"group_name": group_name, "participation_conditions": participation_conditions}
    result = db_client.insert_one(group)

    return {
        "statusCode": 201,
        "body": json.dumps({
            "id": str(result.inserted_id),
            "group_name": group["group_name"],
            "participation_conditions": group["participation_conditions"]
        })
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
