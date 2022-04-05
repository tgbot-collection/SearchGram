#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - config.py
# 4/5/22 09:10
#

__author__ = "Benny <benny.think@gmail.com>"

import os

APP_ID = int(os.getenv("APP_ID", 1234))
APP_HASH = os.getenv("APP_HASH", "1234da")
TOKEN = os.getenv("TOKEN", "abchw")
ES_HOST = os.getenv("ES_HOST", "http://es:9200")
ES_USERNAME = os.getenv("ES_USERNAME", "elastic")
ES_PASSWORD = os.getenv("ES_PASSWORD", "123456")
OWNER_ID = os.getenv("OWNER_ID")
BOT_ID = os.getenv("BOT_ID")
