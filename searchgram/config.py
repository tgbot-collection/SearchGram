#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - config.py
# 4/5/22 09:10
#

__author__ = "Benny <benny.think@gmail.com>"

import os

APP_ID = int(os.getenv("APP_ID", 321232123))
APP_HASH = os.getenv("APP_HASH", "23231321")
TOKEN = os.getenv("TOKEN", "1234")  # id:hash

######### search engine settings #########
# MeiliSearch, by default it's meili in docker-compose
MEILI_HOST = os.getenv("MEILI_HOST", "http://meili:7700")
# Using bot token for simplicity
MEILI_PASS = os.getenv("MEILI_MASTER_KEY", TOKEN)

# If you want to use MongoDB as search engine, you need to set this
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")

# available values: meili, mongo, zinc, default: meili
ENGINE = os.getenv("ENGINE", "meili").lower()

ZINC_HOST = os.getenv("ZINC_HOST", "http://zinc:4080")
ZINC_USER = os.getenv("ZINC_USER", "root")
ZINC_PASS = os.getenv("ZINC_PASS", "root")

####################################
# Your own user id, for example: 260260121
OWNER_ID = os.getenv("OWNER_ID", "260260121")
BOT_ID = int(TOKEN.split(":")[0])

PROXY = os.getenv("PROXY")
# example proxy configuration
# PROXY = {"scheme": "socks5", "hostname": "localhost", "port": 1080}

IPv6 = bool(os.getenv("IPv6", False))
