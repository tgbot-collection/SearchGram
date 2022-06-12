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
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")

PROXY = os.getenv("PROXY")
# example proxy configuration
# PROXY = {"scheme": "socks5", "hostname": "localhost", "port": 1080}
