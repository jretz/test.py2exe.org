= The Problem =

Using [[http://www.reportlab.org|repotlab]] and following the instructions from [[py2exeAndPIL]]. 

Still, when 
{{{
#!python
from reportlab.lib.utils import ImageReader
im=ImageReader(someCstringIOStream())
}}}

raises "cannot identify image file"

= Explanation =

Reportlab does some different things when importing Image from PIL

excerpt from reportlab.lib.utils 
{{{
#!python
class ImageReader:
    "Wraps up either PIL or Java to get data from bitmaps"
    def __init__(self, fileName):
        if not haveImages:
            warnOnce('Imaging Library not available, unable to import bitmaps')
            return
        #start wih lots of null private fields, to be populated by
        #the relevant engine.
        self.fileName = fileName
        self._image = None
        self._width = None
        self._height = None
        self._transparent = None
        self._data = None

        #detect which library we are using and open the image
        if sys.platform[0:4] == 'java':
            from javax.imageio import ImageIO
            if type(fileName) is type(''):
                fp = open(fileName,'rb')
            else:
                fp = fileName
            self._image = ImageIO.read(fp)
        else:
            import PIL.Image
            self._image = PIL.Image.open(fileName)
}}}


= Solution =

Make it dumb. We know: This is not Java, this is Windows. We have PIL, because we use py2exe and ARE responsible to put it into the package. So...


{{{
#!python

class MyImageReader(ImageReader):
    """ Kopie des Report-Lab Image Readers, kommt besser mit
        py2exeter PIL zurande"""
    def __init__(self, fileName):
        #start wih lots of null private fields, to be populated by
        #the relevant engine.
        self.fileName = fileName
        self._image = None
        self._width = None
        self._height = None
        self._transparent = None
        self._data = None

        #änderung: kein Detect oder so, DIES IST WINDOWS
        # PIL IST VORHANDEN
            
        self._image = Image.open(fileName)
}}}

Image has to be imported and "tuned" as described in [[py2exeAndPIL]]

HAM2004-08-09
