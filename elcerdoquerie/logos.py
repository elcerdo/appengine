from models import *
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class DisplayLogo(webapp.RequestHandler):
    def get(self,key):
        try:
            logo = memcache.get("logo/%s"%key)
            if logo is None:
                logo = Logo.get(key)
                try:
                    memcache.add("logo/%s"%key,logo,600)
                except ValueError:
                    logging.error("error setting memcache")
            self.response.headers["Content-type"] = "image/png"
            self.response.out.write(logo.image)
        except db.BadKeyError:
            self.redirect("/static/default.png")

if __name__=="__main__":
    application = webapp.WSGIApplication([("/logos/(.*)",DisplayLogo)],debug=True)
    run_wsgi_app(application)

