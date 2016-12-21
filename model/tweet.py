from model.base_model import BaseModel

__author__ = 'Konstantin Gritsenko <gritsenko.konstantin@gmail.com>'


class Tweet(BaseModel):
    def __init__(self, tweet_id=None, author=None, text=None, timestamp=None):
        """
        :type tweet_id: string
        :type author: string
        :type text: string
        :type timestamp: string
        """
        BaseModel.__init__(self, tweet_id)
        self.author = author
        self.text = text
        self.timestamp = timestamp
