#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - es.py
# 4/4/22 22:08
#

__author__ = "Benny <benny.think@gmail.com>"

import logging

import meilisearch

from config import MEILI_HOST, MEILI_PASS
from engine import BasicSearchEngine
from utils import sizeof_fmt


class SearchEngine(BasicSearchEngine):
    def __init__(self):
        # ["BOT", "CHANNEL", "GROUP", "PRIVATE", "SUPERGROUP"]
        try:
            self.client = meilisearch.Client(MEILI_HOST, MEILI_PASS)
            self.client.create_index("telegram", {"primaryKey": "ID"})
            self.client.index("telegram").update_filterable_attributes(["chat.id", "chat.username", "chat.type"])
            self.client.index("telegram").update_ranking_rules(
                ["timestamp:desc", "words", "typo", "proximity", "attribute", "sort", "exactness"]
            )
            self.client.index("telegram").update_sortable_attributes(["timestamp"])
        except:
            logging.critical("Failed to connect to MeiliSearch")

    def upsert(self, message):
        if self.check_ignore(message):
            return
        data = self.set_uid(message)
        self.client.index("telegram").add_documents([data], primary_key="ID")

    def search(self, keyword, _type=None, user=None, page=1, mode=None) -> dict:
        if mode:
            keyword = f'"{keyword}"'
        user = self.clean_user(user)
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

    def delete_user(self, user):
        params = {
            "filter": [f"chat.username = {user} OR chat.id = {user}"],
            "hitsPerPage": 1000,
        }

        data = self.client.index("telegram").search("", params)
        for hit in data["hits"]:
            self.client.delete_index(hit["ID"])


if __name__ == "__main__":
    search = SearchEngine()
    print(search.delete_user("InfSGK_bot"))
