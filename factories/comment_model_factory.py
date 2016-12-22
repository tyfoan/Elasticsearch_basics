from factories.base_model_factory import BaseModelFactory
from model.comment import Comment

__author__ = 'Konstantin Gritsenko <gritsenko.konstantin@gmail.com>'


class CommentModelFactory(BaseModelFactory):
    def __init__(self):
        BaseModelFactory.__init__(self)

    def get_model(self):
        """
        :rtype: model.comment.Comment
        """
        return Comment()
