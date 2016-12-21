from model.base_model import BaseModel

__author__ = 'Konstantin Gritsenko <gritsenko.konstantin@gmail.com>'


class Comment(BaseModel):
    def __init__(self, comment_id=None, title=None, comment=None, status=None, likes=None, date=None):
        BaseModel.__init__(self, comment_id)
        self.title = title
        self.comment = comment
        self.status = status
        self.likes = likes
        self.date = date
