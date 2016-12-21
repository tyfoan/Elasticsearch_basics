class Tweet:
    def __init__(self, author_id=None, author=None, text=None, timestamp=None):
        self.id = author_id
        self.author = author
        self.text = text
        self.timestamp = timestamp


class Comment:
    def __init__(self, comment_id=None, title=None, comment=None, status=None, likes=None, date=None):
        self.id = comment_id
        self.title = title
        self.comment = comment
        self.status = status
        self.likes = likes
        self.date = date
