import json
import logging

import requests
import azure.functions as func
from datetime import datetime, timedelta
from dotenv import load_dotenv
from dateutil.relativedelta import *
import os

STOCK_API_URL = "https://alpha-vantage.p.rapidapi.com/query"

load_dotenv()

app = func.FunctionApp()


@app.route(route="stocks/{company_symbol}/profit", auth_level="anonymous")
def get_stock_profit(req: func.HttpRequest) -> func.HttpResponse:
    company_symbol = req.route_params.get("company_symbol")
    start_date = req.params.get('start_date')
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if not company_symbol or not start_date:
        return func.HttpResponse(
            "주식 종목의 코드와 시작 일자를 입력해주세요.",
            status_code=400
        )

    time_series = fetch_time_series(company_symbol)
    portfolio = get_portfolio(start_date, time_series)

    return func.HttpResponse(json.dumps(portfolio))


@app.route(route="products", methods=["GET"], auth_level="anonymous")
def get_products(req: func.HttpRequest) -> func.HttpResponse:
    price = float(req.params.get('price'))

    if not price:
        return func.HttpResponse(
            "가격을 입력해주세요.",
            status_code=400
        )

    return func.HttpResponse(json.dumps(get_product_by_price(price)))


def fetch_time_series(company_symbol):
    querystring = {"symbol": company_symbol, "function": "TIME_SERIES_MONTHLY", "datatype": "json"}
    headers = {
        'x-rapidapi-key': os.environ.get("API_KEY"),
        'x-rapidapi-host': "alpha-vantage.p.rapidapi.com"
    }

    response = requests.get(STOCK_API_URL, headers=headers, params=querystring)
    logging.info(response.status_code)
    result = response.json()

    new_data = {}

    for key in result["Monthly Time Series"]:
        new_data[key[:7]] = result["Monthly Time Series"][key]

    return new_data


def get_portfolio(start_date, time_series):
    last_date = datetime.now().strftime('%Y-%m')
    data = buy_stocks_monthly(start_date, time_series)

    return {
        "profit": (float(time_series[last_date]["1. open"]) * data[1]) - data[0],
    }


def buy_stocks_monthly(start_date, time_series):
    current_date = start_date
    total_price = 0
    count = 0

    while current_date <= datetime.now():
        date_str = current_date.strftime('%Y-%m')

        if date_str in time_series.keys():
            count += 1
            total_price += float(time_series[date_str]["1. open"])

        current_date = current_date + relativedelta(months=+1)

    return [total_price, count]


def get_product_by_price(price):
    products = ([
        {"name": "펜", "price": 2,
         "image_url": "https://raw.githubusercontent.com/roharon/book-hackathon-project/master/IfIHaveBoughtStocks/images/pen.jpg"},
        {"name": "피자", "price": 30,
         "image_url": "https://raw.githubusercontent.com/roharon/book-hackathon-project/master/IfIHaveBoughtStocks/images/pizza.jpg"},
        {"name": "아이패드 에어", "price": 599,
         "image_url": "https://raw.githubusercontent.com/roharon/book-hackathon-project/master/IfIHaveBoughtStocks/images/ipad.jpg"},
        {"name": "노트북", "price": 1999,
         "image_url": "https://raw.githubusercontent.com/roharon/book-hackathon-project/master/IfIHaveBoughtStocks/images/laptop.jpg"}
    ])

    products.sort(key=lambda x: x["price"], reverse=True)

    for product in products:
        if price >= product["price"]:
            return {
                "name": product["name"],
                "count": int(price / product["price"]),
                "image_url": product["image_url"]
            }

    return {
        "name": "펜",
        "count": 1,
        "image_url": ""
    }
