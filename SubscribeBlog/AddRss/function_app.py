import json
import logging
import os

import azure.functions as func
import feedparser
import pymongo
from dotenv import load_dotenv

load_dotenv()
DATABASE_NAME = "subscribe_blog"
COLLECTION_NAME = "blogs"
CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")

app = func.FunctionApp()


@app.function_name(name="AddRss")
@app.route(route="AddRss", methods=["POST"], auth_level="anonymous")
def main(req: func.HttpRequest) -> func.HttpResponse:
	if not req.get_body():
		return func.HttpResponse(
			status_code=400
		)

	body_message = json.loads(req.get_body())

	try:
		blog_datum = get_blog_rss(body_message["blog_url"])
		logging.info("blog={}".format(blog_datum))
	except Exception as e:
		return func.HttpResponse(
			status_code=400
		)

	db_client = mongo_client()
	fetched_data = db_client.count_documents({"url": blog_datum["url"]})

	if fetched_data > 0:
		return func.HttpResponse(
			status_code=400
		)

	db_client.insert_one(blog_datum)
	return func.HttpResponse(json.dumps(blog_datum, default=str), mimetype='application/json', status_code=201)


def get_blog_rss(blog_url):
	data = feedparser.parse(blog_url)
	logging.info("blog={}".format(data.feed))
	return {
		"title": data.feed.title,
		"url": data.feed.title_detail.base,
	}


def mongo_client():
	client = pymongo.MongoClient(CONNECTION_STRING)
	db = client[DATABASE_NAME]
	collection = db[COLLECTION_NAME]

	return collection
