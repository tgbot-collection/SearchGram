#!/usr/bin/env python3
# coding: utf-8

# SearchGram - add_timestamp.py
# 2023-05-13  11:26

import logging
import time

from engine import SearchEngine

logging.basicConfig(level=logging.INFO)
s = SearchEngine()


def convert_to_timestamp(date: str) -> int:
    return int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))


limit = 20
offset = 0
index = s.client.index("telegram")
total_documents = index.get_stats().number_of_documents

for offset in range(0, total_documents, limit):
    documents = index.get_documents({"limit": limit, "offset": offset}).results
    for res in documents:
        date_string = res.date
        timestamp = convert_to_timestamp(date_string)
        ID = res.ID
        uid = s.client.index("telegram").update_documents({"ID": ID, "timestamp": timestamp})
        logging.info("Updated %s - %s", res.ID, uid.task_uid)

logging.info("Done")
