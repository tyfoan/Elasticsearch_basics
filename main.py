from elasticsearch import Elasticsearch
import json
from pprint import pprint as pp


class Tweet:
    def __init__(self, author_id=None, author=None, text=None, timestamp=None):
        self.id = author_id
        self.author = author
        self.text = text
        self.timestamp = timestamp


class BaseElasticSearchRepository(object):
    def __init__(self, elastic_search):
        self._elastic_search = elastic_search
        self._index = None
        self._doc_type = None
        # Fields can be extended

    def get_all_query(self):
        return self._elastic_search.search(index=self._index)

    def clear_indexes(self):
        self._elastic_search.indices.delete(index=self._index, ignore=[400, 404])

    def create_index(self, body):
        self._elastic_search.index(index=self._index, doc_type=self._doc_type, body=body, pretty=True)

    def delete_by_id(self, id):
        self.es.delete(self.index, self.doc_type, id)

    def get_sources(self, elasticsearch_request):
        pass

    def convert_search_with_higlight(self, search_result):
        res = []
        hits = search_result['hits']['hits']
        for hit in hits:
            item = {'id': hit['_id']}
            item.update(hit['_source'])
            if 'highlight' in hit:
                [item.update({k: v[0]}) for k, v in hit['highlight'].items()]  # OVERWRITING?
            # fields = hit['_source']
            # if 'highlight' in hit:
            #     item['highlight'] = hit['highlight']
            # for key in fields.keys():
            #     item[key] = fields[key]
            res.append(item)
        return res

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
        return self.convert_search_with_higlight(self._elastic_search.search(self._index, body=query))


class TweetElasticSearchRepository(BaseElasticSearchRepository):
    def __init__(self, elastic_search, index, doc_type):
        BaseElasticSearchRepository.__init__(self, elastic_search)
        self._index = index
        self._doc_type = doc_type
        self._elastic_search = elastic_search

    def get_found_tweet_objects(self, query_string, fields=['content']):
        search_result_items = BaseElasticSearchRepository.search(self, query_string, fields)
        tweets = []
        for result_item in search_result_items:
            tweet = Tweet()
            #setattr(tweets, str(key), value) for key, value in result_item.items()
            for key, value in result_item.items():
                setattr(tweet, str(key), value)
            tweets.append(tweet)
        return tweets


class FileManager:
    def load_objects_from_json_file(self, path):
        documents = []
        with open(path) as o:
            documents = json.load(o)
        return documents


if __name__ == "__main__":
    tweet_elastic_search_repository = TweetElasticSearchRepository(Elasticsearch(), 'messages', 'tweets')
    tweet_elastic_search_repository.clear_indexes()
    file_manager = FileManager()
    json_files = file_manager.load_objects_from_json_file("./indexes.json")
    [tweet_elastic_search_repository.create_index(json) for json in json_files]

    tweets_found = tweet_elastic_search_repository.get_found_tweet_objects('Ok.', ['author', 'text'])
    for tweet in tweets_found:
        pp(tweet.__dict__, indent=4)

    print('-' * 20)

    # json.dumps(dict)
    # all_index_data = tweet_elastic_search_repository.get_all()
    # for item in all_index_data:
    #     pp(item.__dict__, indent=4)
