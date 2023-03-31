#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - init_client.py
# 4/5/22 12:19
#

__author__ = "Benny <benny.think@gmail.com>"

import contextlib
import json
import urllib.request

from pyrogram import Client

from config import APP_HASH, APP_ID, PROXY, IPv6


def get_client(token=None):
    if isinstance(PROXY, str):
        proxy = json.loads(PROXY)
    else:
        proxy = PROXY
    app_device = dict(app_version=f"SearchGram/{get_revision()}", device_model="Firefox", proxy=proxy)
    if token:
        return Client("session/bot", APP_ID, APP_HASH, bot_token=token, ipv6=IPv6, **app_device)
    else:
        return Client("session/client", APP_ID, APP_HASH, ipv6=IPv6, **app_device)


def get_revision():
    url = "https://api.github.com/repos/tgbot-collection/SearchGram/commits/master"
    with contextlib.suppress(Exception):
        return json.loads(urllib.request.urlopen(url).read())["sha"][:7]
    return "0.0.0"
