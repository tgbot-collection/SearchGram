#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - init_client.py
# 4/5/22 12:19
#

__author__ = "Benny <benny.think@gmail.com>"

from pyrogram import Client

from config import APP_HASH, APP_ID


def get_client(token=None):
    proxy = None
    # proxy = {"hostname": "host.docker.internal", "port": 1080}
    if token:
        return Client("session/bot", APP_ID, APP_HASH, bot_token=token,
                      proxy=proxy
                      )
    else:
        return Client("session/client", APP_ID, APP_HASH,
                      proxy=proxy
                      )
