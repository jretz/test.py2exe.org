# Working with Various Packages and Modules

## Biopython

- [Biopython](biopython.md) Fixing problems with importing Bio.Config files from
  library.zip

## cElementTree

- If you're using `import xml.etree.cElementTree`, also use
  `import xml.etree.ElementTree` before that to get it working

## ConfigObj

- ConfigObj does not work right if you installed using easy\_install. Just
  download configobj.py and validate.py from
  <http://www.voidspace.org.uk/python/configobj.htm>

## ctypes.com

- [ctypes DLL servers](../windows/com/ctypes-dll-servers.md) Creating a
  ctypes.com dll com server
- [ctypes EXE servers](../windows/com/ctypes-exe-servers.md) Creating a
  ctypes.com exe com server

## dpkt

- [dpkt](dpkt.md) Fixing problems initializing class attributes

## ftplib

you may need to try including wsock32.dll or winsock.dll. Sometimes one works,
sometimes the other works. Having both might cause problems.

## Innosetup

- [Compression](../guides/optimization/compression.md) Getting complete wxPython
  Programs down to around 4 Megabytes
- [Installer languages](../guides/distribution/installer-languages.md) How to
  localize the language with
  [py2exe](http://starship.python.net/crew/theller/py2exe/) and
  [InnoSetup](http://www.jrsoftware.org/isinfo.php)
- [Installer shortcuts](../guides/distribution/installer-shortcuts.md) How to
  add Startup-Links to the Quickstart-Bar &amp; the Desktop using
  [InnoSetup](http://www.jrsoftware.org/isinfo.php) together with
  [py2exe](../getting-started/overview.md)

## logging module

- [Logging](logging.md) - Getting the %(filename)s format string working in the
  python logging module.

## lxml

- if missing \_elementhpath, either pull whole lxml library in packages=..., or
  put "from lxml import \_elementhpath as \_dummy" somewhere in code; in both
  cases also pull gzip in packages=...

## [Matplotlib](matplotlib.md)

- [Matplotlib](matplotlib.md) - Fixing and including configuration information
  for this plotting package.

## multiprocessing

- See [multiprocessing.freeze\_support][link-1].

## NumPy

- If you're getting *No scipy-style subpackage 'xxx' found in
  c:\\...\\library.zip\\numpy. Ignoring*, try --skip-archive command line option
  or pass **options = {"py2exe": {"skip\_archive":1}}** to setup().
- If you're using numarray and numpy together, be aware that they both have a
  \_sort, and py2exe gets them confused. After py2exe creates the dist
  directotry, copy numpy/core/\_sort.pyd and numarray/sort.pyd to their
  respective locations in the dist. \[This problem is due to a bug in py2exe: it
  used a single, flat namespace for all .pyd files. This has been fixed in CVS
  as of 7 Sep 2007.\]
- Numpy 1.4.0 and Py2exe 0.6.9 may have issues compiling to an executable. The
  executable may run on your computer, but wont run on other machines. You may
  get and error that says the module cant be found or a DLL load failure
  referencing numpy files (.pyc,.pyo). The solution to this is to use numpy
  1.3.0.

## os.popen

- [os.popen](../guides/runtime/os-popen.md) If you're getting failures when the
  CWD is a UNC path like `\\host\dirname\...`

## PIL

- [PIL](pil.md) If you're getting *cannot identify image file*, read this
- [PIL fonts](pil-fonts.md) If you're getting *Cannot find font file*, read this

## protobuf

- [Protobuf](protobuf.md) If you're getting *The following modules appear to be
  missing*

## pubsub

- Add `'pubsub.*', 'pubsub.core.*', 'pubsub.core.kwargs.*'` to
  `include_packages` if using the new interface, otherwise add
  `'pubsub.*', 'pubsub.core.*', 'pubsub.core.arg1.*'` when using the old
  interface.

## PyGTK (and Kiwi)

- [PyGTK](pygtk.md) A recipe for py2exe and PyGTK

## pyodbc

- [pyodbc](pyodbc.md) additional configuration required to include `decimal`
  package

## [PyOpenGL](pyopengl.md)

- [PyOpenGL](pyopengl.md) A hack to get py2exe and [PyOpenGL](pyopengl.md)
  working

## PyQt

- [PyQt](pyqt.md) If you're getting
  `File "qt.pyc", line 7, in __load Import Error: No module named sip`, read
  this

## Python Eggs

- [Python eggs](../guides/build/python-eggs.md) - A recipe for creating an .exe
  out of eggs

## PythonCard

- [PythonCard](pythoncard.md) Getting pythoncard to work by editing setup.py

## Python ADODB modules

- ADODB package Modules named adodb\_xxx (like adodb\_mysql) are not added
  automatically, must be added explicitly

## PyXML

- [PyXML](pyxml.md) If you're getting File "xml\\sax\\saxexts.pyc", line 77, in
  make\_parser; xml.sax.\_exceptions.SAXReaderNotAvailable: No parsers found,
  read this.

## Quixote

Quixote is a pythonivc toolkit for web pages which allows one to execute ptl
files using ihooks. You can distribute your web application with medusa or
twisted and hence you can create a web application without IIS or Apache.

I like to distribute my application with py2exe but I can not make py2exe setup
script to recognize that x.ptl is a valid python files. Any idea how to do this?
\- impossible: [Quixote](quixote.md) HAM20040602

## Raven

It seems Raven uses its own function to import modules and cache them so py2exe
isn't able to figure out which modules are needed. You need to manually specify
them with **options={"py2exe": {"includes": \["raven.events",
"raven.processors"\]}}**.

## reportlab

- [PIL and ReportLab](pil-reportlab.md) If you've read [PIL](pil.md) and still
  get *cannot identify image file*, read this

## SciPy

- [SciPy](scipy.md) Using py2exe with scipy ends up with missing `cephes` and
  `__cvs_version__` messages. Here is a fix.

## subprocess

- [Subprocess](../guides/runtime/subprocess.md) - Getting subprocess module to
  work with py2exe.

## Tix

- [Tix](tix.md) - Including the Tix DLL and Tcl files to make Tix apps work.

## win32com

- [win32com servers](../windows/com/win32com-servers.md) Creating a win32com exe
  and/or dll com server
- [win32com.shell](../windows/com/shell.md) Including with py2exe 0.6
- [Including type libraries](../windows/com/including-typelibs.md) Allowing use
  of makepy generated typelibs
- [EnsureDispatch](../windows/com/ensure-dispatch.md) Use a prog\_id and
  generate 'typelibs' at runtime

## win32pipe

- [win32pipe](../windows/win32pipe.md) (from pywin32) in a bundle.

## win32ui

- [win32ui](../windows/win32ui.md) Using win32ui with py2exe 0.6 and python 2.6

## wxPython

- [wxPython](wxpython.md) If you're getting *wxObjectPtr not found*, read this

## zmq

- [ZeroMQ](zeromq.md) If py2exe cant find libzmq.dll

---

> CategoryCategory

[link-1]: http://docs.python.org/library/multiprocessing.html#multiprocessing.freeze_support
