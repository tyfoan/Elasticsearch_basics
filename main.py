from elasticsearch import Elasticsearch
import json
from pprint import pprint as pp
from collections import namedtuple

class Tweet:
    # def __init__(self, id_author, author, text, timestamp):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

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
            tweets.append(Tweet(**source))
        return tweets

    def delete_all(self):
        self._elastic_search.indices.delete(index=self._index, ignore=[400, 404])

    def create(self, body):
        self._elastic_search.index(index=self._index, doc_type=self._doc_type, body=body, pretty=True)

    def search(self, query_string, fields=['content']):
        list_dict_fields = []
        for i in fields:
            list_dict_fields.append({i: {}})
        query = {
            "query": {
                "multi_match": {
                    "query": query_string,
                    "fields": fields,
                    "operator": "and"
                }
            },
            "highlight": {
                "fields": list_dict_fields,
                "require_field_match": 'false'
            }
        }

        response = self._elastic_search.search(self._index, body=query)

        tweets = []
        for response_item in response['hits']['hits']:
            source = response_item['_source']
            highlights = response_item['highlight']
            tweet = Tweet(**source)
            [setattr(tweet, key, str(value[0])) for key, value in highlights.items()]
            tweets.append(tweet)

        pp(response, indent=4)

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

    tweets_found = elastic_search_repository.search('Ok.', ['author', 'text'])
    for tweet in tweets_found:
        pp(tweet.__dict__, indent=4)

    print('-' * 20)

    # json.dumps(dict)
    all_index_data = elastic_search_repository.get_all()
    for item in all_index_data:
        pp(item.__dict__, indent=4)
