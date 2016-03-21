import os.path
import jinja2
import datetime
from PIL import Image
from cStringIO import StringIO

def dorender(handler, tname='/index.html', values={}):
    templates_dir = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'templates')
    JINJA_ENVIRONMENT = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            extensions=['jinja2.ext.autoescape'],
            autoescape=True)
    def timeJST(value):
        return (value + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S').decode('utf-8')
    JINJA_ENVIRONMENT.filters.update({
        'timeJST':timeJST
    })
    template = JINJA_ENVIRONMENT.get_template(tname[1:])
    handler.response.write(template.render(values))

def writemap(handler, xs, ys):
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
    output = StringIO()
    img.save(output, format='png')
    imagelayer = output.getvalue()
    output.close()
    handler.response.headers['Content-Type'] = 'image/png'
    handler.response.out.write(imagelayer)

def writemap_japan(handler, xs, ys, mapname):
    xs = map(lambda x:10 + (x-128.5988)*965.0/17.2132, xs)
    ys = map(lambda y:15 + (45.5222-y)*1090.0/15.2894, ys)
    img = Image.open(mapname, 'r')
    for i in range(0,len(xs)):
        img.putpixel((int(xs[i]),int(ys[i])),(0,0,255))
    output = StringIO()
    img.save(output, format='png')
    imagelayer = output.getvalue()
    output.close()
    handler.response.headers['Content-Type'] = 'image/png'
    handler.response.out.write(imagelayer)

def writemap_nojapan(handler, xs, ys):
    xs = map(lambda x:10 + (x-128.5988)*965.0/17.2132, xs)
    ys = map(lambda y:15 + (45.5222-y)*1090.0/15.2894, ys)
    img = Image.new('RGB',(1000,1150),(255,255,255))
    for i in range(0,len(xs)):
        img.putpixel((int(xs[i]),int(ys[i])),(0,0,255))
    output = StringIO()
    img.save(output, format='png')
    imagelayer = output.getvalue()
    output.close()
    handler.response.headers['Content-Type'] = 'image/png'
    handler.response.out.write(imagelayer)

