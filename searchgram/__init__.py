#!/usr/bin/env python3
# coding: utf-8

# SearchGram - __init__.py
# 2023-11-18  16:26

from config import ENGINE

if ENGINE == "meili":
    from meili import SearchEngine
elif ENGINE == "mongo":
    from mongo import SearchEngine
