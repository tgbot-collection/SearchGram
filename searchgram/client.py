#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - client.py
# 4/4/22 22:06
#

__author__ = "Benny <benny.think@gmail.com>"

import json
import logging

from pyrogram import Client, filters, types

from config import APP_HASH, APP_ID
from es import TGES

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s %(filename)s:%(lineno)d %(levelname).1s] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = Client("client", APP_ID, APP_HASH,
             proxy={"hostname": "host.docker.internal", "port": 1080}
             )

tges = TGES()


@app.on_message(filters.text & filters.incoming | filters.outgoing)
def message_handler(client: "Client", message: "types.Message"):
    data = json.loads(str(message))
    tges.insert(data)


if __name__ == '__main__':
    app.run()
