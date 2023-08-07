from datetime import date
import boto3

TABLE_NAME = "cafeteria_menu"


def lambda_handler(event, context):
	dynamodb = boto3.client("dynamodb")

	today_date = date.today()
	text = get_meal_text(dynamodb, today_date)

	if text is None:
		return {
			"response_type": "in_channel",
			"blocks": [
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "오늘 점심 메뉴가 없습니다."
					}
				}
			]
		}

	return {
		"response_type": "in_channel",
		"blocks": block_text(text)
	}


def get_meal_text(dynamodb, today_date):
	return dynamodb.get_item(
		TableName=TABLE_NAME, Key={"id": {"S": "{}-lunch".format(today_date.strftime("%Y-%m-%d"))}}
	)["Item"]["menu"]["S"]


def block_text(text):
	return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*점심 메뉴*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": text
			}
		},
	]
