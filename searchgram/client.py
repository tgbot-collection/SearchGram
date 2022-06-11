#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - client.py
# 4/4/22 22:06
#

__author__ = "Benny <benny.think@gmail.com>"

import configparser
import json
import logging
import random
import threading
import time

import fakeredis
from pyrogram import Client, filters, types

from config import BOT_ID
from engine import Mongo
from init_client import get_client
from utils import apply_log_formatter, set_mention

apply_log_formatter()

app = get_client()
tgdb = Mongo()


@app.on_message(filters.outgoing | filters.incoming)
def message_handler(client: "Client", message: "types.Message"):
    # don't know why `~filters.chat(int(BOT_ID))` is not working
    if str(message.chat.id) == BOT_ID:
        logging.debug("Ignoring message from bot itself")
        return

    set_mention(message)
    data = json.loads(str(message))
    tgdb.insert(data)


def safe_edit(msg, new_text):
    key = "sync-chat"
    r = fakeredis.FakeStrictRedis()
    if not r.exists(key):
        time.sleep(random.random())
        r.set(key, "ok", ex=2)
        msg.edit_text(new_text)


def sync_history():
    time.sleep(5)
    section = "chat"
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('sync.ini')

    enable = False
    for _, i in config.items(section):
        if i.lower() != "false":
            enable = True

    if enable:
        saved = app.send_message("me", "Starting to sync history...")

        for uid, enabled in config.items(section):
            if enabled.lower() != "false":
                total_count = app.get_chat_history_count(uid)
                log = f"Syncing history for {uid}"
                logging.info(log)
                safe_edit(saved, log)
                time.sleep(random.random())  # avoid flood
                chat_records = app.get_chat_history(uid)
                current = 0
                for msg in chat_records:
                    safe_edit(saved, f"[{current}/{total_count}] - {log}")
                    current += 1
                    tgdb.update(msg)
                # single chat sync complete, we'll set sync enable to 'false' to avoid further flooding
                config.set(section, uid, 'false')

        with open('sync.ini', 'w') as configfile:
            config.write(configfile)

        log = "Sync history complete"
        logging.info(log)
        safe_edit(saved, log)


if __name__ == '__main__':
    threading.Thread(target=sync_history).start()
    app.run()
