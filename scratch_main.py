import json
from elasticsearch import Elasticsearch
from pprint import pprint as pp


class Elastic_search_repository:
    def __init__(self, elastic_search, index, doc_type):
        self._elastic_search = elastic_search
        self._index = index
        self._doc_type = doc_type

    def create(self, body):
        self._elastic_search.index(index=self._index, doc_type=self._doc_type, body=body)

    def delete_all(self):
        self._elastic_search.indices.delete(index=self._index, ignore=[404, 400])

    def search(self, query_string, fields=['content']):
        fields_dictionary = {}
        for field in fields:
            fields_dictionary[field] = {}

        query_body = {
            "query": {
                "query_string": {
                    'default_field': ','.join(fields),
                    "query": query_string
                }
            },
            "highlight": {
                'fields': fields_dictionary
            }
        }

        result = self._elastic_search.search(self._index, body=query_body)
        pp(result)
        return result


class FileManager:
    def open_file(self, path):
        document = []
        with open(path) as o:
            document = json.load(o)
        return document


if __name__ == '__main__':
    elastic_search = Elastic_search_repository(Elasticsearch(), 'messages', 'tweets')
    # clearing
    elastic_search.delete_all()
    # creating
    file_manager = FileManager()
    [elastic_search.create(json) for json in file_manager.open_file('./indexes.json')]
    # searching
    elastic_search.search('cool.', ['author'])
