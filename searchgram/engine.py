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
    def get_config_list():
        config.read("sync.ini")
        return config.options("whitelist"), config.options("blacklist")

    @staticmethod
    def check_ignore(message):
        whitelist, blacklist = BasicSearchEngine().get_config_list()
        uid = str(message.chat.id)
        chat_type = message.chat.type.name  # upper case
        username = getattr(message.chat, "username", None)
        if whitelist and not (uid in whitelist or username in whitelist or f"`{chat_type}`" in whitelist):
            return True

        if username in blacklist or uid in blacklist or f"`{chat_type}`" in blacklist:
            return True

    @staticmethod
    def clean_user(user: "str"):
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

    def search(self, keyword, _type=None, user=None, page=1, mode=None) -> dict:
        """

        :param keyword:
        :param _type: ChatType.["BOT", "CHANNEL", "GROUP", "PRIVATE", "SUPERGROUP"]
        :param user: username or id
        :param page:
        :param mode: exact match
        :return:
        """

        return {
            "hits": [
                {
                    "ID": "123456-1114100",
                    "_": "Message",
                    "id": 1114100,
                    "from_user": {
                        "_": "User",
                        "id": 260260121,
                        "is_self": True,
                        "is_contact": False,
                        "is_mutual_contact": False,
                        "is_deleted": False,
                        "is_bot": False,
                        "is_verified": False,
                        "is_restricted": False,
                        "is_scam": False,
                        "is_fake": False,
                        "is_support": False,
                        "is_premium": True,
                        "first_name": "Benny小可爱",
                        "status": "UserStatus.ONLINE",
                        "next_offline_date": "2023-11-18 16:35:09",
                        "username": "BennyThink",
                        "emoji_status": {"_": "EmojiStatus", "custom_emoji_id": 5377556559356238807},
                        "dc_id": 5,
                        "phone_number": "*********",
                        "photo": {
                            "_": "ChatPhoto",
                            "small_file_id": "AQADBQADtacxGxlBgw8AEAIAAxlBgw8ABNG47cEZeO_bAAQeBA",
                            "small_photo_unique_id": "AgADtacxGxlBgw8",
                            "big_file_id": "AQADBQADtacxGxlBgw8AEAMAAxlBgw8ABNG47cEZeO_bAAQeBA",
                            "big_photo_unique_id": "AgADtacxGxlBgw8",
                        },
                    },
                    "date": "2023-11-18 16:30:21",
                    "chat": {
                        "_": "Chat",
                        "id": 123456,
                        "type": "ChatType.PRIVATE",
                        "is_verified": False,
                        "is_restricted": False,
                        "is_scam": False,
                        "is_fake": False,
                        "is_support": False,
                        "username": "name_unknow",
                        "first_name": "ok",
                        "photo": {
                            "_": "ChatPhoto",
                            "small_file_id": "edfgh567",
                            "small_photo_unique_id": "ghjgh",
                            "big_file_id": "AQAeBA",
                            "big_photo_unique_id": "AgyebeVQ",
                        },
                        "dc_id": 5,
                    },
                    "mentioned": False,
                    "scheduled": False,
                    "from_scheduled": False,
                    "has_protected_content": False,
                    "text": "测试仪你",
                    "outgoing": True,
                    "timestamp": 1700321421,
                }
            ],
            "query": "测试",
            "processingTimeMs": 1,
            "hitsPerPage": 10,
            "page": 1,
            "totalPages": 1,
            "totalHits": 1,
        }

    def ping(self) -> str:
        pass

    def clear_db(self):
        pass

    def delete_user(self, user):
        pass
