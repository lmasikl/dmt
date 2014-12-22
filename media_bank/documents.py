from mongoengine import Document, StringField


class Post(Document):
    title = StringField()
    body = StringField()