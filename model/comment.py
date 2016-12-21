from model.base_model import BaseModel

__author__ = 'Konstantin Gritsenko <gritsenko.konstantin@gmail.com>'


class Comment(BaseModel):
    def __init__(self, comment_id=None, title=None, comment=None, status=None, likes=None, date=None):
        """
        :type comment_id: string
        :type title: string
        :type comment: string
        :type status: string
        :type likes: int
        :type date: string
        """
        BaseModel.__init__(self, comment_id)
        self.title = title
        self.comment = comment
        self.status = status
        self.likes = likes
        self.date = date
