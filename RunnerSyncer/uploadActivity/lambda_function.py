import urllib.parse

import boto3
from stravalib.client import Client


def lambda_handler(event, _context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    s3 = boto3.client("s3")

    response = s3.get_object(Bucket=bucket, Key=key)
    gpx_raw_value = response["Body"].read().decode("utf-8")
    strava_access_token = response["Metadata"]["strava-access-token"]

    client = Client(access_token=strava_access_token)
    result = client.upload_activity(
        activity_file=gpx_raw_value,
        description="Migrate by RunnerSyncer",
        data_type="gpx",
    )
    print("activity_id={} status={}".format(result.activity_id, result.status))
