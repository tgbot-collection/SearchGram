#!/usr/bin/env python3
# coding: utf-8

# SearchGram - zinc.py
# 2023-11-18  18:04

from utils import sizeof_fmt
import zincsearch_sdk
from engine import BasicSearchEngine


class SearchEngine(BasicSearchEngine):
    def upsert(self, message):
        if self.check_ignore(message):
            return
        data = self.set_uid(message)
        # self.client.index("telegram").add_documents([data], primary_key="ID")

    def search(self, keyword, _type=None, user=None, page=1, mode=None) -> dict:
        pass

    def ping(self) -> str:
        pass

    def clear_db(self):
        pass
