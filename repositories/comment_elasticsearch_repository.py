from model.comment import Comment
from repositories.base_elasticsearch_repository import BaseElasticSearchRepository


class CommentElasticSearchRepository(BaseElasticSearchRepository):
    def get_model(self):
        return Comment()
