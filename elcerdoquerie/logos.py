from models import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class DisplayLogo(webapp.RequestHandler):
    def get(self,key):
        try:
            logo = Logo.get(key)
            self.response.headers["Content-type"] = "image/png"
            self.response.out.write(logo.image)
        except db.BadKeyError:
            self.redirect("/static/default.png")

if __name__=="__main__":
    application = webapp.WSGIApplication([("/logos/([a-zA-z0-9]+)",DisplayLogo)],debug=True)
    run_wsgi_app(application)

