import cgi
import os
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Entry(db.Model):
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class Index(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-type"] = "text/html;utf-8"

        entries = db.GqlQuery("SELECT * FROM Entry ORDER BY date ASC LIMIT 10")
        content = "<p>hello, world!!</p>" + "<ul>" + "".join(["<li>"+cgi.escape(entry.content)+"</li>" for entry in entries]) + "</ul>"

        template_params = { "title": "coucou", "content": content }
        template_path   = os.path.join(os.path.dirname(__file__),"index.html")
        self.response.out.write(template.render(template_path,template_params))

class Sign(webapp.RequestHandler):
    def post(self):
        content = self.request.get('content')
        if content:
            entry = Entry()
            entry.content = content
            entry.put()
        self.redirect("/")

class Clear(webapp.RequestHandler):
    def get(self):
        db.delete(Entry.all())
        self.redirect("/")

application = webapp.WSGIApplication([("/",Index),("/sign",Sign),("/clear",Clear)],debug=True)

if __name__=="__main__":
    run_wsgi_app(application)

