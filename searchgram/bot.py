#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - bot.py
# 4/4/22 22:06
#

__author__ = "Benny <benny.think@gmail.com>"

import logging
import random
import tempfile
import time
from typing import Any, Union

from pyrogram import Client, filters, types

from config import OWNER_ID, TOKEN
from engine import Mongo
from history import HistoryImport
from init_client import get_client
from utils import apply_log_formatter

apply_log_formatter()

tgdb = Mongo()

app = get_client(TOKEN)


def private_use(func):
    def wrapper(client: "Client", message: "types.Message"):
        chat_id = getattr(message.chat, "id", None)
        if chat_id != int(OWNER_ID):
            logging.warning("Unauthorized user: %s", chat_id)
            return
        return func(client, message)

    return wrapper


@app.on_message(filters.command(["start"]))
def search_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, "typing")
    message.reply_text("Hello, I'm search bot.", quote=True)


@app.on_message(filters.command(["ping"]))
@private_use
def ping_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, "typing")
    text = tgdb.ping()
    client.send_message(message.chat.id, text, parse_mode="markdown")


@app.on_message(filters.document & filters.incoming)
@private_use
def import_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, "import_history")
    bot_msg: Union["types.Message", "Any"] = message.reply_text("Staring to import history...", quote=True)
    with tempfile.NamedTemporaryFile() as f:
        client.send_chat_action(message.chat.id, "upload_document")
        message.download(f.name)
        with open(f.name, "rb") as f:
            data = f.read()
        runner = HistoryImport(bot_msg, data)
        runner.load()


@app.on_message(filters.text & filters.incoming)
@private_use
def search_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, "typing")
    results = tgdb.search(message.text)
    for result in results:
        t = "{} on {}\n`{}`".format(result["mention"], result['date'], result['text'])
        time.sleep(random.random())
        client.send_message(message.chat.id, t, parse_mode="markdown")

    if not results:
        client.send_message(message.chat.id, "No results found.")


if __name__ == '__main__':
    app.run()
