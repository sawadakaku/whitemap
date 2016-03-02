import random
from PIL import Image
from cStringIO import StringIO

width,height = 100,100
img = Image.new('RGB',(width+1,height+1),(255,255,255))
for i in range(0,1000):
    img.putpixel((random.randint(0,100),random.randint(0,100)),(0,0,0))
output = StringIO()
img.save(output, format='png')
imagelayer = output.getvalue()
output.close()
print(type(imagelayer))
outfile = open('test.png','w')
outfile.write(imagelayer)
outfile.close()
