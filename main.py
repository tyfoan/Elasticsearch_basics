from elasticsearch import Elasticsearch
import json
from pprint import pprint as pp

from repositories.tweet_elasticsearch_repository import TweetElasticSearchRepository


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
    json_files = file_manager.load_objects_from_json_file("./json_files/tweet.json")
    [tweet_elastic_search_repository.create_index(json) for json in json_files]

    tweets_found = tweet_elastic_search_repository.get_found_tweet_objects('Ok.', ['author', 'text'])
    for tweet in tweets_found:
        pp(tweet.__dict__, indent=4)

    print('-' * 20)

    #comment_elastic_search_repository = CommentElasticSearchRepository(Elasticsearch, 'answers', 'comments')
