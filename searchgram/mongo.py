#!/usr/bin/env python3
# coding: utf-8

# SearchGram - Mongo.py
# 2023-11-18  16:31

__author__ = "Benny <benny.think@gmail.com>"

import math

import pymongo
import zhconv

from config import MONGO_HOST
from engine import BasicSearchEngine
from utils import sizeof_fmt


class SearchEngine(BasicSearchEngine):
    def __init__(self):
        self.client = pymongo.MongoClient(
            host=MONGO_HOST, connect=False, connectTimeoutMS=5000, serverSelectionTimeoutMS=5000
        )
        self.db = self.client["telegram"]
        self.chat = self.db["chat"]

    def __del__(self):
        self.client.close()

    def upsert(self, message):
        if self.check_ignore(message):
            return
        data = self.set_uid(message)
        self.chat.update_one({"ID": data["ID"]}, {"$set": data}, upsert=True)

    def search(self, keyword, _type=None, user=None, page=1, mode=None):
        cond = {}
        hans = zhconv.convert(keyword, "zh-hans")
        hant = zhconv.convert(keyword, "zh-hant")

        if mode:
            # use or exact match search
            cond["$or"] = [{"text": hans}, {"text": hant}]
        else:
            cond["$or"] = [
                {"text": {"$regex": f".*{hans}.*", "$options": "i"}},
                {"text": {"$regex": f".*{hant}.*", "$options": "i"}},
            ]
        user = self.clean_user(user)
        if user:
            cond["$and"] = [
                {
                    "$or": [{"chat.username": user}, {"chat.id": user}],
                }
            ]
        if _type:
            cond["chat.type"] = f"ChatType.{_type}"
        results = self.chat.find(cond).sort("date", pymongo.DESCENDING).limit(10).skip((page - 1) * 10)
        total_hits = self.chat.count_documents(cond)
        total_pages = math.ceil(total_hits / 10)
        return {
            "hits": results,
            "query": keyword,
            "hitsPerPage": 10,
            "page": page,
            "totalPages": total_pages,
            "totalHits": total_hits,
        }

    def ping(self) -> str:
        count = self.chat.count_documents({})
        size = self.db.command("dbstats")["storageSize"]
        return f"{count} messages, {sizeof_fmt(size)}"

    def clear_db(self):
        self.client.drop_database("telegram")

    def delete_user(self, user):
        self.chat.delete_many({"$or": [{"chat.username": user}, {"chat.id": user}]})
