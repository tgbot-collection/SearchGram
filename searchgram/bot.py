#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - bot.py
# 4/4/22 22:06
#

__author__ = "Benny <benny.think@gmail.com>"

import logging

from pyrogram import Client, filters, types

from config import APP_HASH, APP_ID, OWNER_ID, TOKEN
from es import TGES

tges = TGES()
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s %(filename)s:%(lineno)d %(levelname).1s] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = Client("bot", APP_ID, APP_HASH, bot_token=TOKEN,
             proxy={"hostname": "host.docker.internal", "port": 1080}
             )


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
        t = "[{}](tg://user?id={}) on {}\n`{}`".format(
            result["from_user"]["first_name"],
            result['from_user']["id"],
            result['date'],
            result['text'])
        client.send_message(message.chat.id, t, parse_mode="markdown")


if __name__ == '__main__':
    app.run()
