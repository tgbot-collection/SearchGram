#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - client.py
# 4/4/22 22:06
#

__author__ = "Benny <benny.think@gmail.com>"

import json
import logging

from pyrogram import Client, filters, types

from config import BOT_ID, OWNER_ID
from engine import Mongo
from init_client import get_client
from utils import apply_log_formatter

apply_log_formatter()

app = get_client()
tgdb = Mongo()


@app.on_message(filters.outgoing | filters.incoming)
def message_handler(client: "Client", message: "types.Message"):
    # don't know why `~filters.chat(int(BOT_ID))` is not working
    if str(message.chat.id) == BOT_ID:
        logging.debug("Ignoring message from bot itself")
        return

    template = "[{}](tg://user?id={}) to [{}](tg://user?id={})"
    if message.outgoing:
        mention = template.format(
            message.from_user.first_name, message.from_user.id,
            message.chat.first_name, message.chat.id
        )
    else:
        mention = template.format(
            message.from_user.first_name, message.from_user.id,
            "me", OWNER_ID
        )

    caption = message.caption
    if caption:
        setattr(message, "text", caption)

    setattr(message, "mention", mention)
    data = json.loads(str(message))
    tgdb.insert(data)


if __name__ == '__main__':
    app.run()
