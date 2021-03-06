from models import *
import logging
import os
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

def chunk(ll,nn):
    for k in xrange(0,len(ll),nn):
        yield ll[k:k+nn]

class Index(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-type"] = "text/html;utf-8"

        logos = memcache.get("logos")
        if logos is None:
            logos = Logo.all(keys_only=True).order("-date").fetch(35)
            try:
                memcache.add("logos",logos,600)
            except ValueError:
                logging.error("error setting memcache")
        lines = [line for line in chunk(logos,7)]

        entries = Entry.all()

        stats = memcache.get_stats()

        template_params = {"title":"coucou","lines":lines,"entries":entries,"stats":stats}
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

class ClearCache(webapp.RequestHandler):
    def get(self):
        logging.info("clearing memcache")
        memcache.flush_all()
        self.redirect("/")

if __name__=="__main__":
    application = webapp.WSGIApplication([("/",Index),("/sign",Sign),("/clear",Clear),("/clear-cache",ClearCache)],debug=True)
    run_wsgi_app(application)

