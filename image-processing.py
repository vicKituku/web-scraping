from PIL import Image
import os

for f in os.listdir('./images'):
    if f.endswith('.jpg'):
        i = Image.open('./images/'+f)
        fn, fext = os.path.splitext(f)
        i.save('./images/png/{}.png'.format(fn))

# image1 = Image.open('images/image2.jpg')

