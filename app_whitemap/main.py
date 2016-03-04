import os
import binascii
import logging
import webapp2
import xml.etree.ElementTree as ET
from PIL import Image
from cStringIO import StringIO
from webapp2_extras import sessions
from google.appengine.ext import ndb
from modules import mydb
from modules import functions

class SessionEnabledHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

class MainPage(SessionEnabledHandler):
    def get(self):
        functions.dorender(self, '/index.html')

class UploadHandler(SessionEnabledHandler):
    def post(self):
        sessionID = self.session.get('sessionID')
        if not sessionID:
            sessionID = binascii.hexlify(os.urandom(8))
            self.session['sessionID'] = sessionID
        logging.info(self.request.arguments())
        for arg in self.request.arguments():
            route = mydb.Route(parent=ndb.Key('User', sessionID))
            kml = self.request.get(arg)
            route.title = arg
            route.kml = kml
            logging.info(arg)
            route.put()

class WhitemapHandler(SessionEnabledHandler):
    def post(self):
        mapsort = ['japanmap_border.png','japanmap_noborder.png']
        sessionID = self.session.get('sessionID')
        routes_query = mydb.Route.query(ancestor=ndb.Key('User', sessionID))
        routes = routes_query.fetch(limit=100)
        prefix = "{http://www.opengis.net/kml/2.2}"
        coordinate = ''
        for route in routes:
            logging.info(type(route.kml.encode('utf-8')))
            root = ET.fromstring(route.kml.encode('utf-8'))
            coordinate = coordinate + root.find(prefix+"Document").find(prefix+"Placemark").find(prefix+"LineString").find(prefix+"coordinates").text + '\n'
        inp = coordinate.split('\n')
        xs = list()
        ys = list()
        for i in inp:
            s=i[0:-1].split(",")
            if len(s)==3:
                xs.append(float(s[0]))
                ys.append(float(s[1]))
        mapname = self.request.get('mapname')
        if mapname == '2':
            functions.writemap_japandebug(self, xs, ys)
#            functions.writemap(self, xs, ys)
        else:
            functions.writemap_japan(self, xs, ys, mapsort[int(mapname)])


class UpdateHandler(SessionEnabledHandler):
    def get(self):
        sessionID = self.session.get('sessionID')
        try:
            routes_query = mydb.Route.query(ancestor=ndb.Key('User', sessionID))
            routes = routes_query.fetch(limit=100)
            functions.dorender(self, '/routes.html', {'routes':routes})
        except:
            functions.dorender(self, '/routes.html')

config = {}
config['webapp2_extras.sessions'] = {
        'secret_key' : 'my-secret-key'
        }

logging.getLogger().setLevel(logging.DEBUG)

app = webapp2.WSGIApplication([('/upload', UploadHandler),
                               ('/img-whitemap', WhitemapHandler),
                               ('/update', UpdateHandler),
                               ('/.*', MainPage),],
                               config=config,
                               debug=True)
