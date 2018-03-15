import uuid
import datetime
from src.common.database import Database

class Blog(object):
    def __init__(self, author, title, author_id, _id=None):
        self.author = author
        self.author_id = author_id
        self.title = title
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': id})
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]