import datetime
import logging
import os
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Index(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-type"] = "text/html;utf-8"

        template_params = {"title":"coucou"}

        lines = self.request.get('content')
        nprimaries = self.request.get('nprimaries')
        if lines and nprimaries:
            data = {}
            for line in lines.split("\n"):
                try:
                    line = line.strip()
                    line = line.lstrip("#")
                    key,value = line.split("=")
                    data[key.strip()] = value.strip()
                except ValueError:
                    continue

            try:
                nevent = int(data["NumberOfEvents"])
                elapsed = float(data["ElapsedTime"])
                startdate = datetime.datetime.strptime(data["StartDate"],"%a %b %d %H:%M:%S %Y")
                nprimaries = float(nprimaries)
                enddate = startdate + datetime.timedelta(seconds=elapsed/nevent*nprimaries)
                remaining = enddate - ( datetime.datetime.utcnow() + datetime.timedelta(hours=2) )
                template_params["timeresult"] = {}
                template_params["timeresult"]["nevent"] = nevent
                template_params["timeresult"]["elapsed"] = elapsed
                template_params["timeresult"]["startdate"] = startdate
                template_params["timeresult"]["nprimaries"] = nprimaries
                template_params["timeresult"]["progress"] = 100.*nevent/nprimaries
                template_params["timeresult"]["enddate"] = enddate
                template_params["timeresult"]["remaining"] = remaining
            except ValueError:
                pass

        template_path   = os.path.join(os.path.dirname(__file__),"index.html")
        self.response.out.write(template.render(template_path,template_params))

if __name__=="__main__":
    application = webapp.WSGIApplication([("/",Index)],debug=True)
    run_wsgi_app(application)

