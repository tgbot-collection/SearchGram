#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - load_json.py
# 4/5/22 23:26
#

__author__ = "Benny <benny.think@gmail.com>"

import json
import random
import re
import time
import traceback

import fakeredis

from engine import Mongo


class HistoryImport:
    def __init__(self, bm, data):
        self.__bm = bm
        self.text_data = data
        self.__db = Mongo()
        self.__col = self.__db.col
        self.__r = fakeredis.FakeStrictRedis()

    def __del__(self):
        self.__db.client.close()
        self.__r.close()

    @staticmethod
    def __remove_prefix(user_info) -> int:
        return int(re.sub(r"(\D)+", "", user_info))

    def __edit_text(self, new_text):
        key = f"{self.__bm.chat.id}-{self.__bm.message_id}"
        # if the key exists, we shouldn't send edit message
        if not self.__r.exists(key):
            time.sleep(random.random())
            self.__r.set(key, "ok", ex=3)
            self.__bm.edit_text(new_text)

    def __runner(self):
        data = json.loads(self.text_data)
        my_firstname = data.get("personal_information", {}).get("first_name")
        my_id = data.get("personal_information", {}).get("user_id")
        total = current = 0
        for i in data["chats"]["list"]:
            total += len(i["messages"])
        for chat in data["chats"]["list"]:
            self.__edit_text(f"Importing... {current}/{total}")
            template = "[{}](tg://user?id={}) to [{}](tg://user?id={})"
            opposite_name = chat.get("name", chat["type"])
            opposite_uid = chat["id"]
            for msg in chat["messages"]:
                if msg["type"] == "message":
                    if self.__remove_prefix(msg["from_id"]) == my_id:
                        # message I sent, outgoing
                        from_user = {"id": my_id, "first_name": my_firstname, }
                        chat = {"id": opposite_uid, "first_name": opposite_name}
                        mention = template.format(my_firstname, my_id, opposite_name, opposite_uid)
                    else:
                        # incoming message
                        chat = {"id": my_id, "first_name": my_firstname, }
                        from_user = {"id": opposite_uid, "first_name": opposite_name}
                        mention = template.format(opposite_name, opposite_uid, "me", my_id)
                    text_obj = msg["text"]
                    real_text = ""
                    if isinstance(text_obj, str):
                        real_text = text_obj
                    elif isinstance(text_obj, dict):
                        real_text = text_obj["text"]
                    elif isinstance(text_obj, list):
                        for i in text_obj:
                            if isinstance(i, str):
                                real_text += i
                            elif isinstance(i, dict):
                                real_text += i["text"]
                    message = {
                        "message_id": msg["id"],
                        "from_user": from_user,
                        "date": msg["date"],
                        "chat": chat,
                        "text": real_text,
                        "mention": mention,
                    }
                    self.__col.update_one({"message_id": msg["id"]}, {"$set": message}, upsert=True)
                current += 1

        self.__bm.edit_text("✅Import finished")

    def load(self):
        try:
            self.__runner()
        except Exception:
            self.__bm.edit_text("❌Import error\n\n{}".format(traceback.format_exc()))
