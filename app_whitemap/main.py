import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.handlers['Content-Type'] = 'text/plain'
        self.response.handlers('Hello, World!')

class UploadHandler(webapp2.RequestHandler):
    def post(self):
        pass

class WhitemapHandler(webapp2.RequestHandler):
    def get(self):
        pass

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        pass

app = webapp2.WSGIApplication([
    ('/upload', UploadHandler),
    ('/img-whitemap', WhitemapHandler),
    ('/update', UpdateHandler),
    ('/', MainPage),
],debug=True)

