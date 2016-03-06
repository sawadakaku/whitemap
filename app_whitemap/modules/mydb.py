from google.appengine.ext import ndb

class Route(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    kml = ndb.TextProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
