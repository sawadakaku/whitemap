import random
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
        route = mydb.Route(parent=ndb.Key('User', sessionID))
        for arg in self.request.arguments():
            kml = self.request.get(arg)
            route.title = arg
            route.kml = kml
        route.put()

class WhitemapHandler(SessionEnabledHandler):
    def get(self):
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
        logging.info(inp[0])
        for i in inp:
            s=i[0:-1].split(",")
            if len(s)==3:
                xs.append(float(s[0]))
                ys.append(float(s[1]))
        mx = min(xs)
        my = min(ys)
        xs = map(lambda x:x-mx,xs)
        ys = map(lambda x:x-my,ys)
        mx = max(xs)
        my = max(ys)
        width = 1000
        height = width/mx*my
        xs = map(lambda x:x*width/mx, xs)
        ys = map(lambda y:y*height/my,ys)
        height = int(height)

        img = Image.new('RGB',(width+10,height+10),(255,255,255))
        for i in range(0,len(xs)):
            img.putpixel((int(xs[i])+5,height-int(ys[i])+5),(0,0,0))
        #width,height = 100,100
        #img = Image.new('RGB',(width+1,height+1),(255,255,255))
        #for i in range(0,1000):
        #    img.putpixel((random.randint(0,100),random.randint(0,100)),(0,0,0))
        output = StringIO()
        img.save(output, format='png')
        imagelayer = output.getvalue()
        output.close()
        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(imagelayer)

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
