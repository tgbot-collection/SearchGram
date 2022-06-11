#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - es.py
# 4/4/22 22:08
#

__author__ = "Benny <benny.think@gmail.com>"

import json
import re

import pymongo
import zhconv

from config import MONGO_HOST
from utils import set_mention


def sizeof_fmt(num: int, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient(host=MONGO_HOST, connect=False,
                                          connectTimeoutMS=5000, serverSelectionTimeoutMS=5000)
        self.db = self.client["telegram"]
        self.col = self.db["chat"]
        self.history = self.db["history"]

    def __del__(self):
        self.client.close()

    def insert(self, doc: "dict"):
        resp = self.col.insert_one(doc)
        return resp

    @staticmethod
    def __clean_user(user: "str"):
        if user.isdigit():
            return int(user)
        if user.startswith("@"):
            return user[1:]
        if user.startswith("https://t.me/"):
            return user[13:]
        return user

    def search(self, keyword, user=None):
        # support for fuzzy search
        keyword = re.sub(r"\s+", ".*", keyword)

        hans = zhconv.convert(keyword, "zh-hans")
        hant = zhconv.convert(keyword, "zh-hant")
        results = []
        filter_ = {
            "$or":
                [
                    {"text": {'$regex': f'.*{hans}.*', "$options": "-i"}},
                    {"text": {'$regex': f'.*{hant}.*', "$options": "-i"}}
                ]
        }
        if user:
            user = self.__clean_user(user)
            filter_["$and"] = [
                {"$or": [
                    {"from_user.id": user},
                    {"from_user.username": {'$regex': f'.*{user}.*', "$options": "-i"}},
                    {"from_user.first_name": {'$regex': f'.*{user}.*', "$options": "-i"}},

                    {"chat.id": user},
                    {"chat.username": {'$regex': f'.*{user}.*', "$options": "-i"}},
                    {"chat.first_name": {'$regex': f'.*{user}.*', "$options": "-i"}},
                ]}
            ]
        data = self.col.find(filter_)
        for hit in data:
            hit.pop("_id")
            results.append(hit)

        return results

    def ping(self):
        count = self.col.count_documents({})
        size = self.db.command("dbstats")["storageSize"]
        return f"{count} messages, {sizeof_fmt(size)}"

    def insert_history(self, doc):
        self.history.insert_one(doc)

    def find_history(self, msg_id):
        return self.history.find_one({"message_id": msg_id})

    def update(self, doc):
        msg_id = doc.id
        chat_id = doc.chat.id

        set_mention(doc)
        doc = json.loads(str(doc))

        self.col.update_one(
            {
                "chat.id": chat_id,
                "$or": [
                    {"id": {"$eq": msg_id}},
                    {"message_id": {"$eq": msg_id}}
                ]
            },
            {"$setOnInsert": doc},
            upsert=True
        )


if __name__ == '__main__':
    tges = Mongo()
    for i in tges.search("干扰项"):
        print(i["text"], i["mention"])
