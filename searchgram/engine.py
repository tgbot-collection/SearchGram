#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - es.py
# 4/4/22 22:08
#

__author__ = "Benny <benny.think@gmail.com>"

import pymongo

from config import MONGO_HOST


class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient(host=MONGO_HOST, connect=False,
                                          connectTimeoutMS=5000, serverSelectionTimeoutMS=5000)
        self.db = self.client["telegram"]
        self.col = self.db["chat"]

    def __del__(self):
        self.client.close()

    def is_admin(self, username: str) -> bool:
        data = self.db["users"].find_one({"username": username, "group": {"$in": ["admin"]}})
        if data:
            return True

    def is_user_blocked(self, username: str) -> str:
        r = self.db["users"].find_one({"username": username, "status.disable": True})
        if r:
            return r["status"]["reason"]

    def insert(self, doc: "dict"):
        resp = self.col.insert_one(doc)
        return resp

    def search(self, text):
        results = []
        data = self.col.find({"text": {'$regex': f'.*{text}.*', "$options": "-i"}})
        for hit in data:
            hit.pop("_id")
            results.append(hit)

        return results


if __name__ == '__main__':
    tges = Mongo()
    for i in tges.search("醉了"):
        print(i["text"])
