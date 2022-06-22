#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - utils.py
# 4/5/22 12:28
#

__author__ = "Benny <benny.think@gmail.com>"

import logging

from config import OWNER_ID


def apply_log_formatter():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s %(filename)s:%(lineno)d %(levelname).1s] %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def get_fullname(obj):
    # obj is chat or from_user
    name = ""
    if getattr(obj, "first_name", None):
        name += obj.first_name
    if getattr(obj, "last_name", None):
        name += " " + obj.last_name

    name = name.strip()
    if not name:
        name = getattr(obj, "title", "")
    return name


def set_mention(message):
    template = "[{}](tg://user?id={}) to [{}](tg://user?id={})"
    if message.outgoing:
        mention = template.format(
            get_fullname(message.from_user), getattr(message.from_user, "id", 0),
            get_fullname(message.chat), getattr(message.chat, "id", 0)
        )
    else:
        mention = template.format(
            get_fullname(message.from_user), getattr(message.from_user, "id", 0),
            "me", OWNER_ID
        )

    caption = message.caption
    if caption:
        setattr(message, "text", caption)

    setattr(message, "mention", mention)
