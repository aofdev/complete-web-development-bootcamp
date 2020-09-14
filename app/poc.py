from pymongo import MongoClient
from datetime import datetime
import pprint

client = MongoClient("mongodb://root:root@localhost:27017")
db = client["bootcamp"]


def find_one():
    document = db.blogs.find_one({"author": "Stephen R. Covey"})
    pprint.pprint(document)


def find_many():
    for blog in db.blogs.find():
        pprint.pprint(blog)


def insert_one():
    blog = {
        "title": "Think and Grow Rich",
        "author": "Napolean Hill",
        "published_date": datetime(2020, 7, 24, 6, 12, 23)
    }
    inserted_id = db.blogs.insert_one(blog)
    print(inserted_id)


insert_one()
