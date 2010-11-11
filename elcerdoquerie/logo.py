from models import *
import cgi
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

class DetailsLogo(webapp.RequestHandler):
    def get(self,key):
        try:
            logo = Logo.get(key)
            self.response.headers["Content-type"] = "text/xml"
            self.response.out.write("<details><comment>%(comment)s</comment><date>%(date)s</date></details>" % {"comment":cgi.escape(logo.comment),"date":"%d/%d/%d" % (logo.date.month,logo.date.day,logo.date.year)})
        except db.BadKeyError:
            self.error(404)

if __name__=="__main__":
    application = webapp.WSGIApplication([("/logo/(.*)",DisplayLogo),("/details/(.*)",DetailsLogo)],debug=True)
    run_wsgi_app(application)

