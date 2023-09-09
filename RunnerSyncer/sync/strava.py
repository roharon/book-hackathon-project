import io

import requests


def upload_activity(gpx_file_url, access_token) -> dict:
    strava_upload_url = "https://www.strava.com/api/v3/uploads"

    response = requests.get(gpx_file_url)
    gpx_file_raw = io.BytesIO(response.content)

    headers = {"Authorization": "access_token {}".format(access_token)}

    image_data = {"file": ("activity.gpx", gpx_file_raw, "application/gpx+xml")}

    data = {
        "external_id": "RunnerSyncer",
        "description": "Uploaded By RunnerSyncer",
        "data_type": "gpx",
    }

    response = requests.post(
        strava_upload_url, headers=headers, data=data, files=image_data
    )
    return response.json()
