import StringIO
import Image
from bellum.settings import MEDIA_ROOT

def handle_img(imgfile, id, is_alliance):
    '''returns mode in which image was saved. Either 'PNG' or 'GIF' '''
    if is_alliance:
        ipath = 'avatars/a'+str(id)+'.'
    else:
        ipath = 'avatars/u'+str(id)+'.'

    s = ''
    for c in imgfile.chunks():
        s += c

    imagefile  = StringIO.StringIO(s)
    image = Image.open(imagefile)

    # check if our magic is needed:
    if (image.format == 'GIF') and (len(s) < 102400) and (image.size == (32,32)):
        # store as is
        open(MEDIA_ROOT+ipath+'gif', 'wb').write(s)
        return 'GIF'
    else:
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        x = 32
        y = 32

        img_ratio = float(image.size[0]) / image.size[1]

        if x==0.0:
            x = y * img_ratio
        elif y==0.0:
            y = x / img_ratio

        resize_ratio = float(x) / y
        x = int(x); y = int(y)

        if(img_ratio > resize_ratio):
            output_width = x * image.size[1] / y
            output_height = image.size[1]
            originX = image.size[0] / 2 - output_width / 2
            originY = 0
        else:
            output_width = image.size[0]
            output_height = y * image.size[0] / x
            originX = 0
            originY = image.size[1] / 2 - output_height / 2

        #crop
        cropBox = (originX, originY, originX + output_width, originY + output_height)
        image = image.crop(cropBox)

        # resize (doing a thumb)
        image.thumbnail([x, y], Image.ANTIALIAS)

        image.save(MEDIA_ROOT+ipath+'png','PNG')                  # MAGIC ENDS -------------------
        return 'PNG'