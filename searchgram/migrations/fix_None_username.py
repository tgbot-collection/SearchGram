#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - fix_None_username.py
# 6/12/22 10:12
#

__author__ = "Benny <benny.think@gmail.com>"

import sys

sys.path.append("../")
from engine import Mongo
from tqdm import tqdm
from utils import set_mention

tgdb = Mongo()
cond = {"mention": {'$regex': '.*None.*', "$options": "i"}}
data = tgdb.col.find(cond)
total_count = tgdb.col.count_documents(cond)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


for datum in tqdm(data, total=total_count):
    chat_obj = Struct(**datum["chat"])
    from_obj = Struct(**datum["from_user"])
    s = Struct(**{"chat": chat_obj, "from_user": from_obj})
    setattr(s, "outgoing", datum.get("outgoing"))
    setattr(s, "caption", "")
    set_mention(s)
    mention = getattr(s, "mention", None)
    tgdb.col.update_one({"_id": datum["_id"]}, {"$set": {"mention": mention}})

print("Done")
