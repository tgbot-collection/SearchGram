#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - bot.py
# 4/4/22 22:06
#

__author__ = "Benny <benny.think@gmail.com>"

import argparse
import logging
import time

from pyrogram import Client, enums, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import OWNER_ID, TOKEN
from engine import SearchEngine
from init_client import get_client
from utils import setup_logger

setup_logger()
app = get_client(TOKEN)

tgdb = SearchEngine()
parser = argparse.ArgumentParser()
parser.add_argument("keyword", help="the keyword to be searched")
parser.add_argument("-t", "--type", help="the type of message", default=None)
parser.add_argument("-u", "--user", help="the user who sent the message", default=None)
parser.add_argument("-m", "--mode", help="match mode, e: exact match, other value is fuzzy search", default=None)


def private_use(func):
    def wrapper(client: "Client", message: "types.Message"):
        chat_id = getattr(message.chat, "id", None)
        if chat_id != int(OWNER_ID):
            logging.warning("Unauthorized user: %s", chat_id)
            return
        return func(client, message)

    return wrapper


@app.on_message(filters.command(["start"]))
def search_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    message.reply_text("Hello, I'm search bot.", quote=True)


@app.on_message(filters.command(["help"]))
def help_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    help_text = """
SearchGram Search syntax Help:
1. **global search**: send any message to me
2. **chat type search**: `-t=GROUP keyword`, support types are ["BOT", "CHANNEL", "GROUP", "PRIVATE", "SUPERGROUP"]
3. **chat user search**: `-u=user_id|username keyword`
4. **exact match**: `-m=e keyword` or directly `"keyword"`
5. combine of above: `-t=GROUP -u=user_id|username keyword`
    """
    message.reply_text(help_text, quote=True)


@app.on_message(filters.command(["ping"]))
@private_use
def ping_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    text = tgdb.ping()
    client.send_message(message.chat.id, text, parse_mode=enums.ParseMode.MARKDOWN)


def get_name(chat: dict):
    if chat.get("title"):
        return chat["title"]
    # get first_name last_name, if not exist, return username
    first_name = chat.get("first_name", "")
    last_name = chat.get("last_name", "")
    username = chat.get("username", "")
    if first_name or last_name:
        return f"{first_name} {last_name}".strip()
    else:
        return username


def parse_search_results(data: "dict"):
    result = ""
    hits = data["hits"]
    # date field is string, sort using it will be wrong.
    hits.sort(key=lambda x: time.mktime(time.strptime(x["date"], "%Y-%m-%d %H:%M:%S")), reverse=True)

    for hit in hits:
        text = hit.get("text") or hit.get("caption")
        if not text:
            # maybe sticker of media without caption
            continue
        chat_username = get_name(hit["chat"])
        from_username = get_name(hit.get("from_user") or hit["sender_chat"])
        date = hit["date"]
        outgoing = hit["outgoing"]

        if outgoing:
            result += f"{from_username} -> {chat_username} on {date}: \n`{text}`\n"
        else:
            result += f"{chat_username} -> me on {date}: \n`{text}`\n"
    return result


def generate_navigation(page, total_pages):
    if total_pages != 1:
        if page == 1:
            # first page, only show next button
            next_button = InlineKeyboardButton("Next Page", callback_data=f"n|{page}")
            markup_content = [next_button]
        elif page == total_pages:
            # last page, only show previous button
            previous_button = InlineKeyboardButton("Previous Page", callback_data=f"p|{page}")
            markup_content = [previous_button]
        else:
            # middle page, show both previous and next button
            next_button = InlineKeyboardButton("Next Page", callback_data=f"n|{page}")
            previous_button = InlineKeyboardButton("Previous Page", callback_data=f"p|{page}")
            markup_content = [previous_button, next_button]
        markup = InlineKeyboardMarkup([markup_content])
    else:
        markup = None
    return markup


def parse_and_search(text, page=1):
    # return text and markup
    args = parser.parse_args(text.split())
    _type = args.type
    user = args.user
    keyword = args.keyword
    mode = args.mode
    results = tgdb.search(keyword, _type, user, page, mode)
    text = parse_search_results(results)
    if not text:
        return "No results found", None

    total_hits = results["totalHits"]
    total_pages = results["totalPages"]
    page = results["page"]
    markup = generate_navigation(page, total_pages)
    return f"Total Hits: {total_hits}\n{text}", markup


@app.on_message(filters.text & filters.incoming)
@private_use
def search_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    text, markup = parse_and_search(message.text)
    message.reply_text(text, quote=True, parse_mode=enums.ParseMode.MARKDOWN, reply_markup=markup)


@app.on_callback_query(filters.regex(r"n|p"))
def send_method_callback(client: "Client", callback_query: types.CallbackQuery):
    call_data = callback_query.data.split("|")
    direction, page = call_data[0], int(call_data[1])
    message = callback_query.message
    if direction == "n":
        new_page = page + 1
    elif direction == "p":
        new_page = page - 1
    else:
        raise ValueError("Invalid direction")

    # find original user query
    user_query = message.reply_to_message.text
    new_text, new_markup = parse_and_search(user_query, new_page)
    message.edit_text(new_text, reply_markup=new_markup)


if __name__ == "__main__":
    app.run()
