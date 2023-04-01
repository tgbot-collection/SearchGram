#!/usr/bin/env python3
# coding: utf-8

# SearchGram - tests.py
# 2023-04-01  15:18

import unittest

from searchgram.bot import parser


class TestParser(unittest.TestCase):
    def test_simple(self):
        t1 = "message"
        args = parser.parse_args(t1.split())
        self.assertEqual(args.message, "message")

    def test_type(self):
        t1 = "--type=GROUP message"
        args = parser.parse_args(t1.split())
        self.assertEqual(args.type, "GROUP")
        self.assertEqual(args.message, "message")

    def test_user(self):
        t2 = "--user=12345 message"
        args = parser.parse_args(t2.split())
        self.assertEqual(args.user, "12345")
        self.assertEqual(args.message, "message")

    def test_type_and_user(self):
        t3 = "--type=GROUP --user=username message"
        args = parser.parse_args(t3.split())
        self.assertEqual(args.type, "GROUP")
        self.assertEqual(args.user, "username")
        self.assertEqual(args.message, "message")
