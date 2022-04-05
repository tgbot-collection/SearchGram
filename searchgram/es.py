#!/usr/local/bin/python3
# coding: utf-8

# SearchGram - es.py
# 4/4/22 22:08
#

__author__ = "Benny <benny.think@gmail.com>"

from elasticsearch import Elasticsearch

from config import ES_HOST, ES_PASSWORD, ES_USERNAME


class TGES:
    def __init__(self):
        self.es = Elasticsearch(hosts=ES_HOST, verify_certs=False,
                                basic_auth=(ES_USERNAME, ES_PASSWORD)
                                )
        self.index = 'telegram'

    def insert(self, doc):
        resp = self.es.index(index=self.index, document=doc)
        return resp

    def search(self, text):
        results = []
        # automatic Tokenization by es, so we'll use match_phrase
        # resp = self.es.search(index=self.index, query={"match": {"text": text}})
        # q = {"match_phrase": {"text": {"query": text, "slop": 2}}}
        resp = self.es.search(index=self.index, query={"match_phrase": {"text": text}})
        for hit in resp['hits']['hits']:
            results.append(hit["_source"])

        return results


if __name__ == '__main__':
    tges = TGES()
    for i in tges.search("醉了"):
        print(i["text"])
