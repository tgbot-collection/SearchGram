#!/usr/bin/env python3
# coding: utf-8

# SearchGram - add_timestamp.py
# 2023-05-13  11:26

import logging
import time

from tqdm import tqdm

from ..meili import SearchEngine

logging.basicConfig(level=logging.INFO)
s = SearchEngine()


def convert_to_timestamp(date: str) -> int:
    return int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))


limit = 100
offset = 0
index = s.client.index("telegram")
total_documents = index.get_stats().number_of_documents

logging.info("Starting to add timestamp to documents")

with tqdm(total=total_documents) as pbar:
    for offset in range(0, total_documents, limit):
        documents = index.get_documents({"limit": limit, "offset": offset}).results
        for res in documents:
            date_string = res.date
            timestamp = convert_to_timestamp(date_string)
            uid = s.client.index("telegram").update_documents({"ID": res.ID, "timestamp": timestamp})
            pbar.update(1)

logging.info("Done")
