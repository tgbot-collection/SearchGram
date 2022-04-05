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
        resp = self.es.search(index=self.index, body={"query": {"match": {"text": text}}})
        for hit in resp['hits']['hits']:
            results.append(hit["_source"])

        return results


if __name__ == '__main__':
    tges = TGES()
    a = tges.search("哈")
    print(a)
