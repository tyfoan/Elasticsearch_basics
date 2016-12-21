from elasticsearch import Elasticsearch
import json
from pprint import pprint as pp
from factories.tweet_model_factory import TweetModelFactory
from repositories.tweets_repository import TweetsRepository


class FileManager:
    def load_objects_from_json_file(self, path):
        documents = []
        with open(path) as o:
            documents = json.load(o)
        return documents


if __name__ == "__main__":
    tweet_elastic_search_repository = TweetsRepository(Elasticsearch(), 'messages', 'tweets', TweetModelFactory())
    tweet_elastic_search_repository.clear_indexes()
    file_manager = FileManager()
    json_files = file_manager.load_objects_from_json_file("./json_files/tweet.json")
    [tweet_elastic_search_repository.create_index(json) for json in json_files]

    tweets_found = tweet_elastic_search_repository.search('Ok.', ['author', 'text'])
    for tweet in tweets_found:
        pp(tweet.__dict__, indent=4)

    print('-' * 20)

    #comment_elastic_search_repository = CommentElasticSearchRepository(Elasticsearch, 'answers', 'comments')
