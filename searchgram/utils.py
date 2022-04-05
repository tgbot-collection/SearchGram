#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - utils.py
# 4/5/22 12:28
#

__author__ = "Benny <benny.think@gmail.com>"
import logging


def apply_log_formatter():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s %(filename)s:%(lineno)d %(levelname).1s] %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )