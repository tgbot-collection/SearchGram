#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - init_client.py
# 4/5/22 12:19
#

__author__ = "Benny <benny.think@gmail.com>"

from pyrogram import Client

from config import APP_HASH, APP_ID, PROXY


def get_client(token=None):
    if token:
        return Client("session/bot", APP_ID, APP_HASH, bot_token=token,
                      proxy=PROXY
                      )
    else:
        return Client("session/client", APP_ID, APP_HASH,
                      proxy=PROXY
                      )
