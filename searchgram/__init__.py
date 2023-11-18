#!/usr/bin/env python3
# coding: utf-8

# SearchGram - __init__.py
# 2023-11-18  16:26

from config import ENGINE

if ENGINE == "meili":
    print("Using MeiliSearch as search engine")
    from meili import SearchEngine
elif ENGINE == "mongo":
    print("Using MongoDB as search engine")
    from mongo import SearchEngine
