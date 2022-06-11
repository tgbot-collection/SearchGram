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


def set_mention(message):
    template = "[{}](tg://user?id={}) to [{}](tg://user?id={})"
    if message.outgoing:
        mention = template.format(
            getattr(message.from_user, "first_name", None), message.from_user.id,
            message.chat.first_name, message.chat.id
        )
    else:
        mention = template.format(
            getattr(message.from_user, "first_name", None), message.from_user.id,
            "me", OWNER_ID
        )

    caption = message.caption
    if caption:
        setattr(message, "text", caption)

    setattr(message, "mention", mention)
