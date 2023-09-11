import json
import os

from stravalib import Client


def lambda_handler(event, _context):
    client = Client()
    token_response = client.exchange_code_for_token(
        client_id=os.environ["STRAVA_CLIENT_ID"],
        client_secret=os.environ["STRAVA_CLIENT_SECRET"],
        code=event["queryStringParameters"]["code"],
    )

    result = {
        "access_token": token_response["access_token"],
        "refresh_token": token_response["refresh_token"],
        "expires_at": token_response["expires_at"],
    }

    return {"statusCode": 200, "body": json.dumps(result)}
