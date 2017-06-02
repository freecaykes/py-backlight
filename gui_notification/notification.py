import sys
import os
import math
import array
import StringIO
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Notify, GdkPixbuf
from PIL import Image, ImageFont, ImageDraw, ImageOps

class _image(object):

    @staticmethod
    def get_pixbuf(pil_image):
        buff = StringIO.StringIO()
        pil_image.save(buff, 'ppm')
        contents = buff.getvalue()
        buff.close()
        loader = GdkPixbuf.PixbufLoader.new_with_type('pnm')
        loader.write(contents)
        pixbuf = loader.get_pixbuf()
        loader.close()
        return pixbuf

    @staticmethod
    def resize(infile, resize):
        try:
            im = Image.open(infile)
            im.thumbnail(resize, Image.ANTIALIAS)
            # im.save(self.ICON, "JPEG") # rewrite
            return im
        except IOError:
            print "cannot create thumbnail for '%s'" % infile

    @staticmethod
    def invert(image):
        if image.mode == 'RGBA':
            r,g,b,a = image.split()
            rgb_image = Image.merge('RGB', (r,g,b))
            inverted_image = ImageOps.invert(rgb_image)
            r2,g2,b2 = inverted_image.split()
            final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
            return final_transparent_image
        else:
            inverted_image = ImageOps.invert(image)
            return inverted_image

    @staticmethod
    def append(image1, image2):
        images = [image1, image2]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
          new_im.paste(im, (x_offset,0))
          x_offset += im.size[0]

        return new_im


class _brightness_bar_img(object):

    @staticmethod
    def get(level):
        pad = 4 # pixels
        width = 10
        im = Image.new('L', ( 20*(pad+width) + 2*pad, 2*pad + width), 0)
        dr = ImageDraw.Draw(im)

        g_level = int( level / 100 * 20)
        # print level / (100 * 1.0), g_level
        for i in xrange(g_level):
            left_c = (pad + (width+pad) * i, pad)
            right_c = (pad + (width+pad) * (i + 1), pad + width)
            print level, i, left_c, right_c
            dr.rectangle( (left_c, right_c ), fill="white", outline = "black")

        return im


class xbacklight_notification_controller(object):

    APPINDICATOR_ID = 'xBackLight'
    ICON = os.path.abspath(  "./resources/tray_icon.png" )
    ICONSIZE = (256, 256)

    def __init__(self):
        Notify.init("xBackLight")
        self.notification = Notify.Notification().new('')
        self.urgency = 0
        self.thumbnail = GdkPixbuf.Pixbuf.new_from_file( self.ICON )


    def set_urgency(self, level):
        self.urgency = level

    def set_icon(self, path):
        self.ICON = os.path.abspath( path )
        # im = _image.resize( path, self.ICONSIZE )
        self.thumbnail = GdkPixbuf.Pixbuf.new_from_file( self.ICON )

    def set_volume_bar(self, level):
        bar = _image.get_pixbuf( _brightness_bar_img.get(level) )
        # appended = _image.append( self.thumbnail, bar)
        icon = self.thumbnail.copy()
        # appended = GdkPixbuf.Pixbuf.new( GdkPixbuf.Colorspace.RGB , True, 8, bar.get_width() + icon.get_width(), icon.get_height() )
        # icon.composite( appended, 0, 0, appended.get_width(), appended.get_height(), 0, 0, 1.0, 1.0, GdkPixbuf.InterpType.HYPER , 255)
        # bar.composite( appended, 0, 0, appended.get_width(), appended.get_height(), icon.get_width(), icon.get_height()/2, 0.5, 0.5, GdkPixbuf.InterpType.HYPER , 127)

        # # p_bar = _image.get_pixbuf( self.thumbnail )
        self.notification.update("xrandr", str(level) + "%")

        self.notification.set_image_from_pixbuf( icon )


    def show_notification(self):
        self.notification.show()
