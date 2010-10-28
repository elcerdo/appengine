from models import *
import logging
import cgi
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Index(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-type"] = "text/html;utf-8"

        content = "<p>" + "".join(['<img src="/logos/%s" />' % key for key in Logo.all(keys_only=True)]) + "</p>"

        entries = db.GqlQuery("SELECT * FROM Entry ORDER BY date ASC LIMIT 10")
        content += "<p>hello, world!!</p>" + "<ul>" + "".join(["<li>"+cgi.escape(entry.content)+"</li>" for entry in entries]) + "</ul>"

        template_params = {"title":"coucou","content":content}
        template_path   = os.path.join(os.path.dirname(__file__),"index.html")
        self.response.out.write(template.render(template_path,template_params))

class Sign(webapp.RequestHandler):
    def post(self):
        logging.info("adding new entry: %s" % repr(self.request.get('content')))
        content = self.request.get('content')
        if content:
            entry = Entry()
            entry.content = content
            entry.put()
        self.redirect("/")

class Clear(webapp.RequestHandler):
    def get(self):
        logging.info("clearing all entries")
        db.delete(Entry.all())
        self.redirect("/")

if __name__=="__main__":
    application = webapp.WSGIApplication([("/",Index),("/sign",Sign),("/clear",Clear)],debug=True)
    run_wsgi_app(application)

