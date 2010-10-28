all = ["db","Entry"]

from google.appengine.ext import db

class Entry(db.Model):
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class Logo(db.Model):
    image = db.BlobProperty()
    comment = db.StringProperty()
    url = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

