import io
import json
import os

import boto3

from sync import nike


def lambda_handler(event, _context):
    nike_access_token = event["body"]["nike_access_token"]
    strava_access_token = event["body"]["strava_access_token"]

    nike_activity_ids = nike.fetch_activity_ids(nike_access_token)

    session = boto3.Session()
    s3_client = session.client("s3")

    for nike_activity_id in nike_activity_ids:
        gpx_raw_data = fetch_gpx_raw_data_from_nike(nike_activity_id, nike_access_token)

        upload_gpx_to_s3(
            s3_client,
            gpx_raw_data,
            os.environ["S3_BUCKET_NAME"],
            "gpx/{}.gpx".format(nike_activity_id),
            strava_access_token,
        )
        break

    return {"statusCode": 200, "body": json.dumps(nike_activity_ids)}


def fetch_gpx_raw_data_from_nike(nike_activity_id, nike_access_token):
    return (
        nike.fetch_activity_to_gpx(nike_activity_id, nike_access_token)
        .replace("\n", "")
        .replace("\t", "")
        .encode("utf-8")
    )


def upload_gpx_to_s3(
    s3_client, gpx_raw_data: str, bucket: str, key: str, strava_access_token: str
):
    s3_client.upload_fileobj(
        io.BytesIO(gpx_raw_data),
        bucket,
        key,
        ExtraArgs={"Metadata": {"strava-access-token": strava_access_token}},
    )
