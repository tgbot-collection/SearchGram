#!/usr/bin/env python3
# coding: utf-8

# SearchGram - __init__.py
# 2023-11-18  16:26

from config import ENGINE

AVAILABLE_ENGINES = ["meili", "mongo", "zinc"]

if ENGINE == "meili":
    print("Using MeiliSearch as search engine")
    from meili import SearchEngine
elif ENGINE == "mongo":
    print("Using MongoDB as search engine")
    from mongo import SearchEngine
elif ENGINE == "zinc":
    print("Using Zinc as search engine")
    from zinc import SearchEngine
else:
    raise ValueError(f"Unsupported engine {ENGINE}, available engines are {AVAILABLE_ENGINES}")
