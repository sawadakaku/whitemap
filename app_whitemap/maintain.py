import webapp2
import datetime
from google.appengine.ext import ndb
from modules import mydb

ROUTES_LIFE_DAYS = 2

class MaintainDB(webapp2.RequestHandler):
    @staticmethod
    def _deleteDB(target):
        lifetime = datetime.timedelta(days=ROUTES_LIFE_DAYS)
        threshold = datetime.datetime.now() - lifetime
        results = target.query(target.time < threshold)
        list_of_key = ndb.put_multi(results)
        ndb.delete_multi(list_of_key)

class MaintainRouteFiles(MaintainDB):
    def get(self):
        self._deleteDB(mydb.Route)

app = webapp2.WSGIApplication([
    ('/maintain/routefiles',MaintainRouteFiles)
])
