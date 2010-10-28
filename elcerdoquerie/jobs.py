from models import *
import re
import logging
import cgi
import os
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

re_headerimg = re.compile(r'''<img +id=('header-img'|"header-img") +src=['"]([a-z/:.0-9_?=]+)['"] +.*>''')

class Fetch(webapp.RequestHandler):
    def get(self):
        logging.info("fetching reddit logo")
        self.response.headers["Content-type"] = "text/html;utf-8"

        items = []
        def finish_job():
            template_params = {"jobtitle":"reddit logo fetching","items":[stuff for stuff in enumerate(items)]}
            template_path   = os.path.join(os.path.dirname(__file__),"jobs.html")
            self.response.out.write(template.render(template_path,template_params))

        reddit_frontpage = urlfetch.fetch("http://www.reddit.com")
        if reddit_frontpage.status_code != 200:
            items.append({"title":"failed to get reddit frontpage","status":"err"})
            finish_job()
            return
        items.append({"title":"got reddit frontpage","status":"ok","data":cgi.escape(reddit_frontpage.content)})

        match = re_headerimg.search(reddit_frontpage.content)
        if match is None:
            items.append({"title":"failed to find reddit logo image","status":"err"})
            finish_job()
            return
        reddit_logo_url = match.groups()[1]
        items.append({"title":"found reddit logo image","status":"ok","data":'<a href="%s">%s</a>' % (cgi.escape(reddit_logo_url),cgi.escape(reddit_logo_url))})

        reddit_logo =  urlfetch.fetch(reddit_logo_url)
        if reddit_frontpage.status_code != 200:
            items.append({"title":"failed to get reddit logo","status":"err"})
            finish_job()
            return
        items.append({"title":"got reddit logo","status":"ok"})

        logo = Logo()
        logo.comment = "undefined for now"
        logo.image = db.Blob(reddit_logo.content)
        logo.url = reddit_logo_url
        logo.put()
        items.append({"title":"saved reddit logo","status":"ok","data":"key=%s<br/>comment=%s<br/>url=%s" % (logo.key(),cgi.escape(logo.comment),cgi.escape(logo.url))})

        finish_job()

if __name__=="__main__":
    application = webapp.WSGIApplication([("/jobs/fetch-reddit",Fetch)],debug=True)
    run_wsgi_app(application)

