from PIL import Image
from cStringIO import StringIO

img = Image.open('japanmap_noborder.png', 'r')
print(img.size)
#west
for i in range(0,1149):
    img.putpixel((10,i+1),(255,0,0))
#north
for i in range(0,999):
    img.putpixel((i+1,15),(255,0,0))
#east
for i in range(0,1149):
    img.putpixel((975,i+1),(255,0,0))
#south
for i in range(0,999):
    img.putpixel((i+1,1105),(255,0,0))
output = StringIO()
img.save(output, format='png')
imagelayer = output.getvalue()
output.close()
print(type(imagelayer))
outfile = open('test.png','w')
outfile.write(imagelayer)
outfile.close()
