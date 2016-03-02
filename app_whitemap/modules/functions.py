import os.path
import jinja2

def dorender(handler, tname='/index.html', values={}):
    templates_dir = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'templates')
    JINJA_ENVIRONMENT = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            extensions=['jinja2.ext.autoescape'],
            autoescape=True)
    template = JINJA_ENVIRONMENT.get_template(tname[1:])
    handler.response.write(template.render(values))
