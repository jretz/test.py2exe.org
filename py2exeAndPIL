= The Problem =

I use [[http://www.pythonware.com/products/pil/|PIL]] from pythonware. It has some very dynamic initialising routines.

excerpt out of Image.py
{{{
#!python
def init():
    "Load all file format drivers."

    global _initialized
    if _initialized >= 2:
        return

    visited = {}

    directories = sys.path

    try:
        directories = directories + [os.path.dirname(__file__)]
    except NameError:
        pass

    # only check directories (including current, if present in the path)
    for directory in filter(isDirectory, directories):
        fullpath = os.path.abspath(directory)
        if visited.has_key(fullpath):
            continue
        for file in os.listdir(directory):
            if file[-14:] == "ImagePlugin.py":
                f, e = os.path.splitext(file)
                try:
                    sys.path.insert(0, directory)
                    try:
                        __import__(f, globals(), locals(), [])
                    finally:
                        del sys.path[0]
                except ImportError:
                    if DEBUG:
                        print "Image: failed to import",
                        print f, ":", sys.exc_value
        visited[fullpath] = None

    if OPEN or SAVE:
        _initialized = 2

}}}

main problem with all this stuff: all this directory-voodoo is out of access when using py2exe. Maybe it is fixable by doing very strange things I do not know about.

= Explanation =

PIL tries to automagically learn which Image-Plugins are available. "available" is well defined as long it is a Python standard installation.
"available" gets very vague when using py2exe.

= Solution =

Make it dumb.

{{{
#!python
# PIL schafft das nicht alleine, wenn gepy2exed
import Image
import PngImagePlugin
[...]
Image._initialized=2
}}}

before using PIL, I manually import Image and also the needed *ImagePlugins
{{{
#!python
[...] could be JpegImagePlugin, BmpImagePlugin etc.
}}}
Finally I force Image to believe it is fully initialized, so nobody tries directory scanning.

