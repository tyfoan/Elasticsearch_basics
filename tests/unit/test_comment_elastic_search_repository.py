import unittest
from factories.comment_model_factory import CommentModelFactory
from mockito import mock, when, any
from model.comment import Comment
from repositories.base_elasticsearch_repository import BaseElasticSearchRepository

__author__ = 'Konstantin Gritsenko <gritsenko.konstantin@gmail.com>'


class TestCommentElasticSearchRespository(unittest.TestCase):
    def setUp(self):
        self._highlighted_text = "some highlighted text"
        """Setup all needed objects"""
        self._elastic_search = mock()
        when(self._elastic_search)\
            .search(any(), body=any())\
            .thenReturn(self._prepare_search_reponse())
        self._repository = BaseElasticSearchRepository(
            self._elastic_search,
            "some_test_index",
            "some_test_doc_type",
            CommentModelFactory()
        )
        pass

    def test_search_with_highlight(self):
        result = self._repository.search("some query string")
        expected_results = self._prepare_expected_data()
        for item, expected_item in zip(result, expected_results):
            self.assertEquals(expected_item.__dict__, item.__dict__)

    def _prepare_data(self):
        return [
            Comment("1", "qwerty 1", "qazxsw 1", "plmnko 1", "qazxsw 1", "plmnko 1"),
            Comment("2", "qwerty 2", "qazxsw 2", "plmnko 2", "qazxsw 1", "plmnko 1"),
            Comment("3", "qwerty 3", "qazxsw 3", "plmnko 3", "qazxsw 1", "plmnko 1"),
            Comment("4", "qwerty 4", "qazxsw 4", "plmnko 4", "qazxsw 1", "plmnko 1"),
            Comment("5", "qwerty 5", "qazxsw 5", "plmnko 5", "qazxsw 1", "plmnko 1"),
        ]

    def _prepare_expected_data(self):
        return [
            Comment("1", self._highlighted_text, self._highlighted_text, self._highlighted_text, self._highlighted_text, self._highlighted_text),
            Comment("2", self._highlighted_text, self._highlighted_text, self._highlighted_text, self._highlighted_text, self._highlighted_text),
            Comment("3", self._highlighted_text, self._highlighted_text, self._highlighted_text, self._highlighted_text, self._highlighted_text),
            Comment("4", self._highlighted_text, self._highlighted_text, self._highlighted_text, self._highlighted_text, self._highlighted_text),
            Comment("5", self._highlighted_text, self._highlighted_text, self._highlighted_text, self._highlighted_text, self._highlighted_text),
        ]

    def _prepare_search_reponse(self):
        return {
            "hits": {
                "hits": [
                    {
                        '_id': item.id,
                        '_source': {
                            'title': item.title,
                            'comment': item.comment,
                            'status': item.status,
                            'likes': item.likes,
                            'date': item.date,
                        },
                        'highlight': {
                            'title': [self._highlighted_text],
                            'comment': [self._highlighted_text],
                            'status': [self._highlighted_text],
                            'likes': [self._highlighted_text],
                            'date': [self._highlighted_text],
                        }
                    } for item in self._prepare_data()
                ]
            }
        }
