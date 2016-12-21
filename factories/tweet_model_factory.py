from factories.base_model_factory import BaseModelFactory
from model.tweet import Tweet

__author__ = 'Konstantin Gritsenko <gritsenko.konstantin@gmail.com>'


class TweetModelFactory(BaseModelFactory):
    def __init__(self):
        BaseModelFactory.__init__(self)

    def get_model(self):
        """
        :rtype: model.tweet.Tweet
        """
        return Tweet()
