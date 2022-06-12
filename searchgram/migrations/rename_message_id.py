#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - rename_message_id.py
# 6/12/22 11:11
#

__author__ = "Benny <benny.think@gmail.com>"

import sys

sys.path.append("../")
from engine import Mongo
from utils import set_mention
from tqdm import tqdm

tgdb = Mongo()
cond = {"message_id": {"$exists": True}}
count = tgdb.col.count_documents(cond)
data = tgdb.col.find(cond)

for item in tqdm(data, total=count):
    msg_id = item["message_id"]
    tgdb.col.update_one({"_id": item["_id"]}, {"$unset": {"message_id": ""}, "$set": {"id": msg_id}})

print("Done")
