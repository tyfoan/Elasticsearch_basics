from model.tweet import Tweet
from repositories.base_elasticsearch_repository import BaseElasticSearchRepository


class TweetElasticSearchRepository(BaseElasticSearchRepository):
    def get_model(self):
        return Tweet()
