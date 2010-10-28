__all__ = ["db","Logo","Entry"]

from google.appengine.ext import db

class Entry(db.Model):
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class Logo(db.Model):
    image = db.BlobProperty(default=None)
    comment = db.StringProperty()
    url = db.StringProperty()
    mainpage = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
