# PyQt

## Error message

```py2tb
  File "form1.pyc", line 11, in ?
  File "qt.pyc", line 9, in ?
  File "qt.pyc", line 7, in __load
ImportError: No module named sip
```

## Solution

`python setup.py py2exe --includes sip`

## setup.py

```python
from py2exe.build_exe import py2exe
from distutils.core import setup
setup( console=[{"script": "main.py"}] )
```

## Reference

I found this tips here :
<http://nerdierthanthou.nfshost.com/2005/03/image-resizer.html>

There is a full code sample.

## Another Solution to the same problem&#58;

```python2
from distutils.core import setup
import py2exe
setup(windows=[{"script":"main.py"}], options={"py2exe":{"includes":["sip"]}})
```

I found that on the web, unfortunately don't know anymore where, but it also
works for me!

Obviously is the second part only a way to get the " --includes sip" parameter
directly into the script, but the use of "windows" instead of "console" doesn't
open a console window, but immediately a Qt window in my case.

## Fix for PyQt4

If you get the following error:

```output
ImportError: No module named _qt
```

The solution is to add PyQt4.\_qt to the setup function (see bellow). I found
the solution for the problem
here (<https://www.mail-archive.com/pyqt@riverbankcomputing.com/msg11417.html>).

```python
from distutils.core import setup
import py2exe

setup(windows=[{"script" : "app.pyw"}], options={"py2exe" : {"includes" : ["sip", "PyQt4._qt"]}})
```

## Using PyQt4 with Databases

When deploying applications which use PyQt4 and SQLite:

- Add "PyQt4.QtSql' to the setup includes.
- Copy the contents of PyQt4\\plugins\\sqldrivers to &lt;appdir&gt;\\sqldrivers.
  It did not work for me in any subdirectory including the zipfile directory.
  For SQLite I only needed to copy qsqlite4.dll.
- A separate copy of sqlite3.dll is not needed.

**Tips**: use data\_files for this. See below

## PyQt4 and Phonon

In a similar manner as using PyQt4 and SQlite (from pyqt), one need to add an
extra step to use Phonon and copy PyQt4\\plugins\\phonon\_backend directory into
your dist directory. Otherwise you get an error: "phonon backend could not be
loaded"

But the correct way to do this is to use
[Data files](../guides/build/data-files.md) in your setup.py

```python2
data_files = [
            ('phonon_backend', [
                'C:\Python26\Lib\site-packages\PyQt4\plugins\phonon_backend\phonon_ds94.dll'
                ])
]
```

## PyQt4 and image loading (JPG, GIF, etc)

PyQt4 uses plugins to read those image formats, so you'll need to copy the
folder PyQt4\\plugins\\imageformats to &lt;appdir&gt;\\imageformats. Like in the
above cases, you can use data\_files for this. This won't work with
bundle\_files on.

If the plugins are not reachable, then QPixmap.load/loadFromData will return
False when loading an image in those formats.

This will work with bundle\_files as well, but you need to exclude the Qt DLLs
from bundle (using the `dll_excludes` option) and add them to the directory with
the executable through some other mechanism (such as `data_files`).
