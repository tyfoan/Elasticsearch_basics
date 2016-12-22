import unittest
from factories.tweet_model_factory import TweetModelFactory
from mockito import mock, when, any
from model.tweet import Tweet
from repositories.base_elasticsearch_repository import BaseElasticSearchRepository

__author__ = 'Konstantin Gritsenko <gritsenko.konstantin@gmail.com>'


class TestTweetElasticSearchRespository(unittest.TestCase):
    def setUp(self):
        self._highlighted_text = "some highlighted text"
        """Setup all needed objects"""
        self._elastic_search = mock()
        pass

    def test_search_with_highlight(self):
        when(self._elastic_search).search(any(), body=any()).thenReturn(self._prepare_search_reponse(True))
        self._repository = BaseElasticSearchRepository(self._elastic_search, "some_test_index", "some_test_doc_type", TweetModelFactory())

        result = self._repository.search("some query string")
        expected_results = self._prepare_expected_data()
        for item, expected_item in zip(result, expected_results):
            self.assertEquals(expected_item.__dict__, item.__dict__)

    def test_search_without_highlight(self):
        when(self._elastic_search).search(any(), body=any()).thenReturn(self._prepare_search_reponse())
        self._repository = BaseElasticSearchRepository(self._elastic_search, "some_test_index", "some_test_doc_type", TweetModelFactory())

        result = self._repository.search("some query string")
        expected_results = self._prepare_data()
        for item, expected_item in zip(result, expected_results):
            self.assertEquals(expected_item.__dict__, item.__dict__)

    def _prepare_data(self):
        return [
            Tweet("1", "qwerty 1", "qazxsw 1", "plmnko 1"),
            Tweet("2", "qwerty 2", "qazxsw 2", "plmnko 2"),
            Tweet("3", "qwerty 3", "qazxsw 3", "plmnko 3"),
            Tweet("4", "qwerty 4", "qazxsw 4", "plmnko 4"),
            Tweet("5", "qwerty 5", "qazxsw 5", "plmnko 5"),
        ]

    def _prepare_expected_data(self):
        return [
            Tweet("1", self._highlighted_text, self._highlighted_text, "plmnko 1"),
            Tweet("2", self._highlighted_text, self._highlighted_text, "plmnko 2"),
            Tweet("3", self._highlighted_text, self._highlighted_text, "plmnko 3"),
            Tweet("4", self._highlighted_text, self._highlighted_text, "plmnko 4"),
            Tweet("5", self._highlighted_text, self._highlighted_text, "plmnko 5"),
        ]

    def _prepare_search_reponse(self, with_highlight=False):
        search_response = {
            "hits": {
                "hits": [
                    {
                        '_id': item.id,
                        '_source': {
                            'author': item.author,
                            'text': item.text,
                            'timestamp': item.timestamp
                        }
                    } for item in self._prepare_data()
                ]
            }
        }
        if with_highlight:
            for item in search_response['hits']['hits']:
                item['highlight'] = {
                    'author': [self._highlighted_text],
                    'text': [self._highlighted_text]
                }
        return search_response
