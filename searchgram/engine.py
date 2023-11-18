#!/usr/bin/env python3
# coding: utf-8

# SearchGram - engine.py
# 2023-11-18  16:34

import configparser
import contextlib
import json

config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = lambda option: option


class BasicSearchEngine:
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

    def upsert(self, message):
        pass

    def search(self, keyword, _type=None, user=None, page=1, mode=None):
        pass

    def ping(self) -> str:
        pass

    def clear_db(self):
        pass
