#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - bot.py
# 4/4/22 22:06
#

__author__ = "Benny <benny.think@gmail.com>"

import logging
import random
import time

from pyrogram import Client, filters, types

from config import OWNER_ID, TOKEN
from es import TGES
from init_client import get_client
from utils import apply_log_formatter

apply_log_formatter()
tges = TGES()

app = get_client(TOKEN)


@app.on_message(filters.command(["start"]))
def search_handler(client: "Client", message: "types.Message"):
    # process as chat.id, not from_user.id
    message.reply_text("Hello, I'm search bot.", quote=True)


@app.on_message(filters.text & filters.incoming)
def search_handler(client: "Client", message: "types.Message"):
    # process as chat.id, not from_user.id
    if message.chat.id != int(OWNER_ID):
        logging.warning("Unauthorized user: %s", message.from_user.id)
        return
    results = tges.search(message.text)
    for result in results:
        t = "{} on {}\n`{}`".format(result["mention"], result['date'], result['text'])
        time.sleep(random.random())
        client.send_message(message.chat.id, t, parse_mode="markdown")


if __name__ == '__main__':
    app.run()
