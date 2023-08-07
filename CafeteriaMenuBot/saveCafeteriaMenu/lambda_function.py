from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
import re
import requests
import boto3
import os

CLOVA_OCR_URL = os.environ['CLOVA_OCR_URL']
CAFETERIA_MENU_URL = (
    "https://gbmo.go.kr/chungsa/dv/dietView/selectDietCalendarView.do?mi=1277&gbd=CD002"
)


def lambda_handler(event, context):
    data = process_ocr(fetch_image_url())
    menus = parse_menu(data)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cafeteria_menu')

    with table.batch_writer() as batch:
        plus_days = 0
        for index, menu in enumerate(menus):
            if (index > 1) and (index % 2 == 0):
                plus_days += 1

            specific_date = datetime.today() + timedelta(days=plus_days)
            meal_type = 'lunch' if index % 2 == 0 else 'dinner'

            print(specific_date.strftime("%Y-%m-%d") + '-' + meal_type)
            batch.put_item(Item={
                'id': specific_date.strftime("%Y-%m-%d") + '-' + meal_type,
                'menu': menu
                }
            )

    return {
        'statusCode': 200
    }


def fetch_image_url():
    page = requests.get(CAFETERIA_MENU_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    image_file_name = soup.find("div", "scl_img").img["src"]

    return "https://gbmo.go.kr" + image_file_name


def process_ocr(image_url):
    headers = {
        "Content-Type": "application/json",
        "X-OCR-SECRET": os.environ['CLOVA_OCR_SECRET']
    }
    payload = json.dumps(
        {
            "images": [
                {
                    "format": "png", "name": "medium",
                    "data": None, "url": image_url
                }
            ],
            "lang": "ko",
            "requestId": "string",
            "resultType": "string",
            "timestamp": 1690734374,
            "version": "V2",
            "enableTableDetection": True,
        }
    )

    response = requests.post(CLOVA_OCR_URL, headers=headers, data=payload)
    return response.json()


def parse_menu(data):
    menus = []
    temporary_menu = []

    for i in data['images'][0]['tables'][0]['cells']:
        if len(i['cellTextLines']) >= 1:
            infer_text = i['cellTextLines'][0]['cellWords'][0]['inferText']
            temporary_menu.append(i['cellTextLines'][0]['cellWords'][0]['inferText'])

            if 'kcal' in infer_text:
                text = "\n".join(temporary_menu)
                match = re.search(r'\d{2}월 (\d{2}일)?\n?', text)
                start_index = 0
                if match is not None:
                    start_index = match.end()
                menus.append(text[start_index:])
                temporary_menu = []

    return menus
