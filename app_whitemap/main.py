import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.handlers['Content-Type'] = 'text/plain'
        self.response.handlers('Hello, World!')

app = webapp2.WSGIApplication([
    ('/', MainPage),
],debug=True)
