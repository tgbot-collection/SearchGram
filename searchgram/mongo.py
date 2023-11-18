#!/usr/bin/env python3
# coding: utf-8

# SearchGram - Mongo.py
# 2023-11-18  16:31

__author__ = "Benny <benny.think@gmail.com>"

import contextlib
import json
import re

import pymongo
import zhconv

from config import MONGO_HOST
from utils import sizeof_fmt

from engine import BasicSearchEngine


class SearchEngine(BasicSearchEngine):
    def __init__(self):
        self.client = pymongo.MongoClient(host=MONGO_HOST, connect=False, connectTimeoutMS=5000, serverSelectionTimeoutMS=5000)
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
        pass

    def search2(self, keyword, _type=None, user=None, page=1, mode=None):
        # support for fuzzy search
        keyword = re.sub(r"\s+", ".*", keyword)

        hans = zhconv.convert(keyword, "zh-hans")
        hant = zhconv.convert(keyword, "zh-hant")
        results = []
        filter_ = {"$or": [{"text": {"$regex": f".*{hans}.*", "$options": "i"}}, {"text": {"$regex": f".*{hant}.*", "$options": "i"}}]}
        if user:
            user = self.__clean_user(user)
            filter_["$and"] = [
                {
                    "$or": [
                        {"from_user.id": user},
                        {"from_user.username": {"$regex": f".*{user}.*", "$options": "i"}},
                        {"from_user.first_name": {"$regex": f".*{user}.*", "$options": "i"}},
                        {"chat.id": user},
                        {"chat.username": {"$regex": f".*{user}.*", "$options": "i"}},
                        {"chat.first_name": {"$regex": f".*{user}.*", "$options": "i"}},
                    ]
                }
            ]
        data = self.col.find(filter_).sort("date", pymongo.DESCENDING)
        for hit in data:
            hit.pop("_id")
            results.append(hit)

        return results

    def ping(self) -> str:
        count = self.chat.count_documents({})
        size = self.db.command("dbstats")["storageSize"]
        return f"{count} messages, {sizeof_fmt(size)}"

    def clear_db(self):
        self.client.drop_database("telegram")


if __name__ == "__main__":
    tges = SearchEngine()
    for i in tges.search("干扰项"):
        print(i["text"], i["mention"])
