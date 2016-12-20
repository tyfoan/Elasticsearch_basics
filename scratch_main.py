from elasticsearch import Elasticsearch
import json
from pprint import pprint as pp


# 1. write this code from scratch
# 2. convert sources to object AND write to result object
class Tweet:
    def __init__(self, id_author, author, text, timestamp):
        self.id = id_author
        self.author = author
        self.text = text
        self.timestamp = timestamp



class ElasticSearchRepository:
    def __init__(self, elastic_search, index, doc_type):
        self._index = index
        self._doc_type = doc_type
        self._elastic_search = elastic_search

    def get_all(self):
      # source = self._elastic_search.get(index=self._index)
        tweets_response = self._elastic_search.search(index=self._index)
        tweets = []
        for tweet in tweets_response['hits']['hits']:
            source = tweet['_source']
            tweets.append(Tweet(tweet['_id'], source['author'], source['text'], source['timestamp']))
        return tweets

    def delete_all(self):
        self._elastic_search.indices.delete(index=self._index, ignore=[400, 404])

    def create(self, body):
        self._elastic_search.index(index=self._index, doc_type=self._doc_type, body=body, pretty=True)

    def search(self, query_string, fields=['content']):
        dict_fields = {}
        for i in fields:
            dict_fields[i] = {}
        query = {
            "query": {
                "query_string": {
                    "default_field": ','.join(fields),
                    "query": query_string
                }
            },
            "highlight": {
                "fields": dict_fields
            }
        }
        #print query
        response = self._elastic_search.search(self._index, body=query)
        #pp(response)

        tweets = []
        for response_item in response['hits']['hits']:
            source = response_item['_source']
            tweets.append(Tweet(response_item['_id'], source['author'], source['text'], source['timestamp']))

#        for i in tweets:
#            self._elastic_search.index

        return tweets


class FileManager:
    def load_objects_from_json_file(self, path):
        documents = []
        with open(path) as o:
            documents = json.load(o)
        return documents


if __name__ == "__main__":
    elastic_search_repository = ElasticSearchRepository(Elasticsearch(), 'messages', 'tweets')
    elastic_search_repository.delete_all()
    file_manager = FileManager()
    json_files = file_manager.load_objects_from_json_file("./indexes.json")
    [elastic_search_repository.create(json) for json in json_files]

    tweets_found = elastic_search_repository.search('Ok.', ['text'])
    for tweet in tweets_found:
        print tweet.id
        print tweet.author
        print tweet.text

    print '-'*20

    all_tweets = elastic_search_repository.get_all()
    for tweet in all_tweets:
        print tweet.id
        print tweet.author
        print tweet.text
        print '*'*5
