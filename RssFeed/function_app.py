import json
import os
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from time import mktime

import azure.functions as func
import feedparser
import html2text
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()
DATABASE_NAME = "RssFeed"
BLOG_COLLECTION_NAME = "blogs"
ARTICLE_COLLECTION_NAME = "articles"
CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")

app = func.FunctionApp()


@app.route(route="rss", methods=["POST"], auth_level="anonymous")
def add_rss(req: func.HttpRequest) -> func.HttpResponse:
    if not req.get_body():
        return func.HttpResponse(

        )

    body_message = json.loads(req.get_body())

    try:
        blog_datum = get_blog_rss(body_message["blog_url"])
    except Exception as e:
        return func.HttpResponse(
            status_code=400
        )

    db_client = mongo_client()[BLOG_COLLECTION_NAME]
    fetched_data = db_client.count_documents({"link": blog_datum["link"]})

    if fetched_data > 0:
        return func.HttpResponse(
            status_code=400
        )

    db_client.insert_one(blog_datum)
    return func.HttpResponse(status_code=201)


@app.route(route="rss", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_rss(req: func.HttpRequest) -> func.HttpResponse:
    db_client = mongo_client()[BLOG_COLLECTION_NAME]
    blogs = list(db_client.find())

    return func.HttpResponse(json.dumps(blogs, default=str), status_code=200)


@app.route(route="rss/{id}", methods=["DELETE"], auth_level=func.AuthLevel.ANONYMOUS)
def delete_rss(req: func.HttpRequest) -> func.HttpResponse:
    blog_id = req.route_params.get("id")
    db_client = mongo_client()[BLOG_COLLECTION_NAME]
    db_client.delete_one({"_id": ObjectId(blog_id)})

    return func.HttpResponse(status_code=200)


@app.route(route="rss/feed", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_rss_feed(req: func.HttpRequest) -> func.HttpResponse:
    db_client = mongo_client()[ARTICLE_COLLECTION_NAME]
    articles = list(db_client.find().sort("published_at", pymongo.DESCENDING).limit(30))

    result = []

    for article in articles:
        result.append(
            {
                "title": article["title"],
                "summary": article["summary"],
                "link": article["link"],
                "published_at": datetime.fromtimestamp(article["published_at"],
                                                       timezone(timedelta(hours=9))).isoformat()
            }
        )

    return func.HttpResponse(json.dumps(result, default=str), status_code=200)


@app.timer_trigger(schedule="0 */10 * * * *", arg_name="mytimer", run_on_startup=True,
                   use_monitor=False)
def fetch_articles(mytimer: func.TimerRequest) -> None:
    db_client = mongo_client()[ARTICLE_COLLECTION_NAME]

    blogs = list(mongo_client()[BLOG_COLLECTION_NAME].find())

    for blog in blogs:
        rss_data = feedparser.parse(blog["link"])
        blog_index = db_client.find_one({"blog_id": blog["_id"]}, sort=[("published_at", pymongo.DESCENDING)])

        last_fetched_article_published_at = (
            db_client.find_one({"blog_id": blog["_id"]},
                               sort=[("published_at", pymongo.DESCENDING)]).get(
                "published_at", None)) if blog_index is not None else None

        articles = fetch_blog_articles(rss_data.entries, last_fetched_article_published_at)
        if len(articles) > 0:
            db_client.insert_many([{**article, "blog_id": blog["_id"]} for article in articles])

    return None


def get_blog_rss(blog_url):
    data = feedparser.parse(blog_url)
    return {
        "title": data.feed.title,
        "description": data.feed.description,
        "link": data.feed.title_detail.base
    }


def fetch_blog_articles(entries: list, last_fetched_article_published_at: int = None):
    articles = []
    html_to_text = html2text.HTML2Text()
    html_to_text.ignore_links = True

    for entry in entries:
        entry_published_at = mktime(entry.published_parsed)
        if last_fetched_article_published_at and entry_published_at <= last_fetched_article_published_at:
            break

        articles.append({
            "title": entry.title,
            "summary": html_to_text.handle(entry.summary),
            "link": entry.link,
            "published_at": entry_published_at
        })

    return articles


def mongo_client():
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]

    return db
