#!/usr/bin/env python3
# coding: utf-8

# SearchGram - zinc.py
# 2023-11-18  18:04

import math

import zincsearch_sdk
from zincsearch_sdk.api import document, index, search
from zincsearch_sdk.model.meta_bool_query import MetaBoolQuery
from zincsearch_sdk.model.meta_match_query import MetaMatchQuery
from zincsearch_sdk.model.meta_query import MetaQuery
from zincsearch_sdk.model.meta_query_string_query import MetaQueryStringQuery
from zincsearch_sdk.model.meta_zinc_query import MetaZincQuery

from config import ZINC_HOST, ZINC_PASS, ZINC_USER
from engine import BasicSearchEngine
from utils import sizeof_fmt

configuration = zincsearch_sdk.Configuration(host=ZINC_HOST, username=ZINC_USER, password=ZINC_PASS)

api_client = zincsearch_sdk.ApiClient(configuration)
INDEX = "telegram"


class SearchEngine(BasicSearchEngine):
    def upsert(self, message):
        if self.check_ignore(message):
            return
        data = self.set_uid(message)
        api_instance = document.Document(api_client)
        api_instance.index_with_id(INDEX, data.get("ID"), data)

    def search(self, keyword, _type=None, user=None, page=1, mode=None) -> dict:
        query = MetaZincQuery(
            query=MetaQuery(
                bool=MetaBoolQuery(
                    must=[
                        MetaQuery(
                            query_string=MetaQueryStringQuery(query=keyword),
                        ),
                    ],
                ),
            ),
            sort=["-@timestamp"],
            _from=(page - 1) * 10,
            size=10,
            track_total_hits=True,
        )

        user = self.clean_user(user)
        if user:
            query.query.bool.must.append(
                MetaQuery(
                    bool=MetaBoolQuery(
                        should=[
                            MetaQuery(match={"chat.username": MetaMatchQuery(query=str(user))}),
                            MetaQuery(match={"chat.id": MetaMatchQuery(query=str(user))}),
                        ]
                    )
                )
            )
        if _type:
            query.query.bool.must.append(MetaQuery(match={"chat.type": MetaMatchQuery(query=f"ChatType.{_type}")}))

        if mode:
            pass
            # TODO exact match, use term query?

        api_instance = search.Search(api_client)
        results = api_instance.search(INDEX, query)
        total_hits = results.hits.total.value
        total_pages = math.ceil(total_hits / 10)
        return {
            "hits": results.hits.hits,
            "query": keyword,
            "hitsPerPage": 10,
            "page": page,
            "totalPages": total_pages,
            "totalHits": total_hits,
        }

    def ping(self) -> str:
        api_instance = index.Index(api_client)
        api_response = api_instance.get_index(INDEX)
        size = api_response["stats"]["storage_size"]
        count = api_response["stats"]["doc_num"]
        return f"{count} messages, {sizeof_fmt(size)}"

    def clear_db(self):
        api_instance = index.Index(api_client)
        api_instance.delete(INDEX)

    def delete_user(self, user):
        raise NotImplementedError


if __name__ == "__main__":
    engine = SearchEngine()
    r = engine.search("天才啊", _type="PRIVATE")
    print(engine.ping())
    engine.clear_db()
