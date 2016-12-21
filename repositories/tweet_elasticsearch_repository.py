from model.models import Tweet
from repositories.base_elasticsearch_repository import BaseElasticSearchRepository


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
            for key, value in result_item.items():
                setattr(tweet, str(key), value)
            tweets.append(tweet)
        return tweets
