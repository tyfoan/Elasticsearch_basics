from repositories.base_elasticsearch_repository import BaseElasticSearchRepository


class CommentElasticSearchRepository(BaseElasticSearchRepository):
    def __init__(self, elastic_search, index, doc_type):
        BaseElasticSearchRepository.__init__(self, elastic_search)
        self._index = index
        self._doc_type = doc_type
        self._elastic_search = elastic_search
