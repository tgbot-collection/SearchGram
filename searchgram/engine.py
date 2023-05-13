#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - es.py
# 4/4/22 22:08
#

__author__ = "Benny <benny.think@gmail.com>"

import configparser
import contextlib
import json
import logging

import meilisearch

from config import MEILI_HOST, MEILI_PASS
from utils import setup_logger, sizeof_fmt

setup_logger()
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = lambda option: option


class SearchEngine:
    def __init__(self):
        # ["BOT", "CHANNEL", "GROUP", "PRIVATE", "SUPERGROUP"]
        try:
            self.client = meilisearch.Client(MEILI_HOST, MEILI_PASS)
            self.client.create_index("telegram", {"primaryKey": "ID"})
            self.client.index("telegram").update_filterable_attributes(["chat.id", "chat.username", "chat.type"])
            self.client.index("telegram").update_sortable_attributes(["timestamp"])
        except:
            logging.critical("Failed to connect to MeiliSearch")

    @staticmethod
    def set_uid(message) -> "dict":
        uid = f"{message.chat.id}-{message.id}"
        timestamp = int(message.date.timestamp())
        setattr(message, "ID", uid)
        setattr(message, "timestamp", timestamp)

        data = json.loads(str(message))
        return data

    @staticmethod
    def check_ignore(message):
        config.read("sync.ini")
        blacklist = config.options("blacklist")
        whitelist = config.options("whitelist")
        uid = str(message.chat.id)
        chat_type = message.chat.type.name  # upper case
        username = getattr(message.chat, "username", None)
        if whitelist and not (uid in whitelist or username in whitelist or f"`{chat_type}`" in whitelist):
            return True

        if username in blacklist or uid in blacklist or f"`{chat_type}`" in blacklist:
            return True

    def upsert(self, message):
        if self.check_ignore(message):
            return
        data = self.set_uid(message)
        self.client.index("telegram").add_documents([data])

    @staticmethod
    def __clean_user(user: "str"):
        if user is None:
            return None
        with contextlib.suppress(Exception):
            return int(user)
        if user.startswith("@"):
            return user[1:]
        if user.startswith("https://t.me/"):
            return user[13:]
        return user

    def search(self, keyword, _type=None, user=None, page=1, mode=None):
        if mode:
            keyword = f'"{keyword}"'
        user = self.__clean_user(user)
        params = {
            "hitsPerPage": 10,
            "page": page,
            "sort": ["timestamp:desc"],
            "matchingStrategy": "all",
            "filter": [],
        }
        if user:
            params["filter"].extend([f"chat.username = {user} OR chat.id = {user}"])
        if _type:
            params["filter"].extend([f"chat.type = ChatType.{_type}"])
        logging.info("Search params: %s", params)
        return self.client.index("telegram").search(keyword, params)

    def ping(self):
        text = "Pong!\n"
        stats = self.client.get_all_stats()
        size = stats["databaseSize"]
        last_update = stats["lastUpdate"]
        for uid, index in stats["indexes"].items():
            text += f"Index {uid} has {index['numberOfDocuments']} documents\n"
        text += f"\nDatabase size: {sizeof_fmt(size)}\nLast update: {last_update}\n"
        return text

    def clear_db(self):
        self.client.index("telegram").delete()


if __name__ == "__main__":
    search = SearchEngine()
    print(search.search("猫"))
