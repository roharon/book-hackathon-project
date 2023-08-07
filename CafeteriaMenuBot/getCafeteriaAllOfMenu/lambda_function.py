from datetime import date
import boto3

TABLE_NAME = "cafeteria_menu"


def lambda_handler(event, context):
	dynamodb = boto3.client("dynamodb")

	today_date = date.today()
	lunch_text = get_meal_text(dynamodb, today_date, "lunch")
	dinner_text = get_meal_text(dynamodb, today_date, "dinner")

	blocks = []
	
	if lunch_text is not None:
		blocks.extend(block_text(lunch_text, "lunch"))

	if dinner_text is not None:
		blocks.extend(block_text(dinner_text, "dinner"))

	if len(blocks) == 0:
		return {
			"response_type": "in_channel",
			"blocks": [
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "오늘 식당 메뉴가 없습니다."
					}
				}
			]
		}

	return {
		"response_type": "in_channel",
		"blocks": blocks
	}


def get_meal_text(dynamodb, today_date, meal_type):
	return dynamodb.get_item(
		TableName=TABLE_NAME, Key={"id": {"S": "{}-{}".format(today_date.strftime("%Y-%m-%d"), meal_type)}}
	)["Item"]["menu"]["S"]


def block_text(text, meal_type):
	return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*점심 메뉴*" if meal_type == "lunch" else "*저녁 메뉴*"
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
