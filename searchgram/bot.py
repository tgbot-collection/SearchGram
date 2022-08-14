#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - bot.py
# 4/4/22 22:06
#

__author__ = "Benny <benny.think@gmail.com>"

import logging
import tempfile
from typing import Any, Union

from pyrogram import Client, enums, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import OWNER_ID, TOKEN
from engine import Mongo
from history import HistoryImport
from init_client import get_client
from utils import apply_log_formatter

apply_log_formatter()

tgdb = Mongo()

app = get_client(TOKEN)


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


@app.on_message(filters.command(["user"]))
@private_use
def search_in_user_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    if message.text == "/user":
        message.reply_text("Command format: /user username|id|firstname keyword")
        return

    _, user, keyword = message.text.split(maxsplit=2)
    results = tgdb.search(keyword, user)
    send_search_results(message.chat.id, results)


@app.on_message(filters.command(["ping"]))
@private_use
def ping_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    text = tgdb.ping()
    client.send_message(message.chat.id, text, parse_mode=enums.ParseMode.MARKDOWN)


@app.on_message(filters.document & filters.incoming)
@private_use
def import_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    bot_msg: Union["types.Message", "Any"] = message.reply_text("Staring to import history...", quote=True)
    with tempfile.NamedTemporaryFile() as f:
        client.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
        message.download(f.name)
        with open(f.name, "rb") as f2:
            data = f2.read()
        runner = HistoryImport(bot_msg, data)
        runner.load()


@app.on_message(filters.text & filters.incoming)
@private_use
def search_handler(client: "Client", message: "types.Message"):
    client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    results = tgdb.search(message.text)
    send_search_results(message.chat.id, results)


def send_search_results(chat_id, results):
    if not results:
        app.send_message(chat_id, "No results found.")
        return

    next_button = InlineKeyboardButton(
        "Next Page",
        callback_data="n|0"  # current index
    )
    final = ""
    for result in results:
        final += "{} on {}\n`{}`\r".format(result["mention"], result['date'], result['text'])
    list_data = final.split("\r")
    length = 1000
    group_data = []
    element = ""
    for text in list_data:
        if len(element) + len(text) <= length:
            element += f"{text}\n"
        else:
            group_data.append(element)
            element = f"{text}\n"
        if list_data.index(text) == len(list_data) - 1:
            group_data.append(element)

    if not group_data:
        group_data = [element]
    if len(group_data) > 1:
        markup = InlineKeyboardMarkup(
            [
                [
                    next_button
                ]
            ]
        )
    else:
        markup = None

    hint = "**Total {} pages.**\n\n".format(len(group_data))
    bot_msg = app.send_message(chat_id, hint + group_data[0], parse_mode=enums.ParseMode.MARKDOWN, reply_markup=markup)
    tgdb.insert_history({"message_id": bot_msg.id, "messages": group_data})


@app.on_callback_query(filters.regex(r"n|p"))
def send_method_callback(client: "Client", callback_query: types.CallbackQuery):
    call_data = callback_query.data.split("|")
    direction, cursor = call_data[0], int(call_data[1])
    message = callback_query.message
    if direction == "n":
        cursor += 1
    elif direction == "p":
        cursor -= 1
    else:
        raise ValueError("Invalid direction")
    data = tgdb.find_history(message.id)
    current_data = data["messages"][cursor]
    total_count = len(data["messages"])

    next_button = InlineKeyboardButton(
        "Next Page",
        callback_data=f"n|{cursor}"
    )
    previous_button = InlineKeyboardButton(
        "Previous Page",
        callback_data=f"p|{cursor}"
    )

    if cursor == 0:
        markup_content = [next_button]
    elif cursor + 1 == total_count:
        markup_content = [previous_button]
    else:
        markup_content = [previous_button, next_button]

    markup = InlineKeyboardMarkup([markup_content])
    message.edit_text(current_data, reply_markup=markup)


if __name__ == '__main__':
    app.run()
