from google.appengine.ext import ndb

class Route(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    kml = ndb.TextProperty()
