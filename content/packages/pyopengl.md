# PyOpenGL

As of PyOpenGL 3.0, add the following to any of your python files to get py2exe
to work.

```python2
from ctypes import util
try:
    from OpenGL.platform import win32
except AttributeError:
    pass
```

The following was not necessary for me.

[PyOpenGL](http://pyopengl.sourceforge.net/) is a set of Python bindings for the
OpenGL graphical rendering library. It has
[a page on how to compile with py2exe][link-1], but it is outdated. Here's how I
made it work for me, although it is quite wasteful in space.

- In your `setup.py`, exclude `OpenGL` although you have PyOpenGL installed. I
  needed to explicitly include `ctypes` and `logging` to make it work, but maybe
  that depends on what things you use. My `setup.py`:

```python2
from distutils.core import setup
import py2exe

setup(windows=['opdracht.py'],
      options={
          "py2exe": {
              "includes": ["ctypes", "logging"],
              "excludes": ["OpenGL"],
              }
          }
      )
```

- At the top of your main Python file, add the current directory (`'.'`) to your
  `sys.path`:

```python2
import sys
sys.path += ['.']
```

- Run `setup.py py2exe`.
- Copy the `OpenGL` folder from PYTHONDIR`\Lib\site-packages` to your new
  `dist\` directory. I think it's in `C:\Python26\Lib\site-packages` by default.
  You can leave out any \*.pyc and \*.pyo files.

I think that's what did the trick for me, now . If you need funky stuff like TK,
WGL, or OpenGLContext, maybe [the original tutorial by PyOpenGL][link-2] helps.

Tested with Python 2.6, py2exe version 0.6.9 and PyOpenGL version 3.0.0.

--- [Bram Geron](mailto:bgeron@gmail.com)

[link-1]: http://pyopengl.sourceforge.net/documentation/py2exe.html
[link-2]: http://pyopengl.sourceforge.net/documentation/py2exe.html
