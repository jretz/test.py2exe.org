# py2exe

Py2Exe is an additional command to
[Distutils](https://docs.python.org/2.7/library/distutils.html), that creates
standalone distributions for Win32.
Latest version as of 2006-March-20 is 0.6.5

Its home is here [Home](../index.md) and on Sourceforge
<https://sourceforge.net/projects/py2exe/>

Releases can be downloaded from <https://sourceforge.net/projects/py2exe/files/>

## How does py2exe work and what are all those files?

Let's start from the needed results going back to how py2exe does its job.

Python is an interpreted language and as long as Microsoft will not ship a
Python interpreter (and its accompanying class library) with every copy of its
flagship operating systems products, there is no direct way to execute a Python
script on a vanilla Microsoft OS machine.
For most casual user of py2exe, that means that you must create an executable
(.exe) file that when clicked on will just run the script.
This is what py2exe does for you.
After py2exe has done its magic, you should have a "dist" directory with all the
files necessary to run your python script. No install necessary. Click and run.
No DLL hell, nothing else to download.

But what are all those files?

|  |  |
| --- | --- |
| myprog.exe | The actual executable. You can select a custom icon by using some specific target options (see [Icons](../guides/build/icons.md)) |
| python??.dll | the python interpreter library. This is the brain of your executable |
| library.zip | This is a standard zip file where all the pure source modules will be inserted (using the "zipfile" option, you can also select to put that file in a sub-directory and with a different name) |
| \*.pyd | The pyd files are actually standard Windows DLL (I used the useful depends.exe to check things around). They are also standard modules for Python. A Python program can import those pyd. Some applications build pyd to provide accelerated features. Also they are necessary to provide support to native functions of the operating system (see also CTypes to never have to use SWIG again!). Those files also follow into the subdirectory where library.zip will be installed |
| \*.dll | some pyd probably have some DLL dependencies, and here they come |
| w9xpopen.exe | This is needed on Win9x platform. |

To run your program needs all those files as a necessary condition. But it might
happen that this is not a sufficient condition. For examples, as encodings are
imported "by name". If you use a feature that requires encodings, you will need
to put an option to include encodings unconditionally or to import it explicitly
from one of your script. (see
[Missing encodings](../troubleshooting/missing-encodings.md) and
[Default encoding](../troubleshooting/default-encoding.md)).
Some other modules (eg [pyserial-pyparallel](http://pyserial.sourceforge.net/))
also conditionally import modules for each platform. You can avoid the warning
by putting the correct "ignores" options in py2exe. Last but not least, modules
like [pygtk](https://wiki.gnome.org/Projects%282f%29PyGTK.html) seem to create a
module reference on-the-fly
and therefore the corresponding warnings also are harmless (see
[Excluding DLLs](../guides/build/excluding-dlls.md) to learn how to correct
that).

An important point to note: the main script (the one passed as an option to
"windows" or "console" in your setup file) is not put with all the other files
in the library.zip. Instead it is byte-compiled (see
[Optimized bytecode](../guides/optimization/optimized-bytecode.md) for some
details on optimization) and inserted into a named resource in the executable
shell. This technique also allows you to insert binary string in the final
executable (very nice if you want to add a custom version tag) through the usage
of the "other\_resources" options for the target (see
[Embedded resources](../guides/build/embedded-resources.md)).

## Learned things with py2exe 0.5

[py2exe0.5.0][link-1] is the release of py2exe 0.5
[announced][link-2] by Thomas Heller in January 2004

As nearly usual in Open Source space, prereleases and beta are of the same
quality as .02 releases from some commercial software developing companies -
rather full functional, with small obstacles.

I had to "upgrade" also my knowledge about workarounds from py2exe 0.4

[Windows services](../windows/services.md) - some gained knowledge

## Tips and Tricks

### General

- [Options](../guides/build/options.md) How to see the list of available options
  for your setup.py script
- [Running setup](running-setup.md) How to run the setup script once you've
  written it
- [Missing encodings](../troubleshooting/missing-encodings.md) Problem with
  encodings and when they are not found in a standalone executable
- [Default encoding](../troubleshooting/default-encoding.md) They really keep
  bugging. Solution to problem with different site.py
- [Configuration files](../guides/build/configuration-files.md) How can you add
  arbitrary files to your Py2Exe-Setup?
- [Path module](../packages/path-module.md) Using Jason Orendorffs python
  [Path module](../packages/path-module.md) together with Py2Exe 0.5
- [Passing options](../guides/build/passing-options.md) Avoid using sys.argv to
  pass options
- [Customizing the build](../guides/build/customizing-the-build.md) Customizing
  the build process
- [Icons](../guides/build/icons.md) How to get your own icons with Py2Exe 0.5
- [Tkinter](../packages/tkinter.md) I do not need any tkinter / tcl-Libs in my
  Setup
- [Filename case](../troubleshooting/filename-case.md) Some windows filing
  systems mangle case, break py2exe programs
- [Batch builds](../guides/build/batch-builds.md) A short Windows Batch File to
  fast provide the EXE File
- [Excluding DLLs](../guides/build/excluding-dlls.md) Stopping py2exe from
  picking up unwanted DLLs
- [Embedded Python](../guides/distribution/embedded-python.md) How to use py2exe
  to ship embedded Python modules
- [Single file executables](../guides/distribution/single-file-executables.md)
  with NSIS
- [Optimized bytecode](../guides/optimization/optimized-bytecode.md) How to get
  optimized bytecode for all modules
- [Embedded resources](../guides/build/embedded-resources.md) Add custom data in
  the executable?
- [Detecting frozen programs](../guides/runtime/detecting-frozen-programs.md)
  Simple functions to determine if you're in an .exe or .py
- [Locating the executable](../guides/runtime/locating-the-executable.md)
  sometimes you need to now where your exe is within the filesystem

### py2exe and PyQt

- [PyQt](../packages/pyqt.md) If you're getting
  `File "qt.pyc", line 7, in __load Import Error: No module named sip`, read
  this

### py2exe and wxPython

- [wxPython](../packages/wxpython.md) If you're getting *wxObjectPtr not found*,
  read this

### py2exe and PyGTK

- [PyGTK](../packages/pygtk.md) A recipe for py2exe and PyGTK

### py2exe and PIL

- [PIL](../packages/pil.md) If you're getting *cannot identify image file*, read
  this

### py2exe and reportlab

- [PIL and ReportLab](../packages/pil-reportlab.md) If you've read
  [PIL](../packages/pil.md) and still get *cannot identify image file*, read
  this

### py2exe and Python ADODB modules

- ADODB package Modules named adodb\_xxx (like adodb\_mysql) are not added
  automatically, must be added explicitly

### py2exe and PyXML

- [PyXML](../packages/pyxml.md) If you're getting *File "xml\\sax\\saxexts.pyc",
  line 77, in make\_parser; xml.sax.\_exceptions.SAXReaderNotAvailable: No
  parsers found*, read this.

### py2exe and win32com

- [win32com servers](../windows/com/win32com-servers.md) Creating a win32com exe
  and/or dll com server
- [win32com.shell](../windows/com/shell.md) Using the shell module with py2exe
- [Including type libraries](../windows/com/including-typelibs.md) Allowing use
  of makepy generated typelibs

### py2exe and ctypes.com

- [ctypes DLL servers](../windows/com/ctypes-dll-servers.md) Creating a
  ctypes.com dll com server
- [ctypes EXE servers](../windows/com/ctypes-exe-servers.md) Creating a
  ctypes.com exe com server

### py2exe and Innosetup

- [Compression](../guides/optimization/compression.md) Getting complete wxPython
  Programs down to around 4 Megabytes
- [Installer languages](../guides/distribution/installer-languages.md) How to
  localize the language with
  [py2exe](https://sourceforge.net/projects/py2exe/files/) and
  [InnoSetup](https://jrsoftware.org/isinfo.php)
- [Installer shortcuts](../guides/distribution/installer-shortcuts.md) How to
  add Startup-Links to the Quickstart-Bar &amp; the Desktop using
  [InnoSetup](https://jrsoftware.org/isinfo.php) together with Py2Exe

### py2exe and Biopython

- [Biopython](../packages/biopython.md) Fixing problems with importing
  Bio.Config files from library.zip

### py2exe and SciPy

- [SciPy](../packages/scipy.md) Using py2exe with scipy ends up with missing
  `cephes` and `__cvs_version__` messages. Here is a fix.

### py2exe and PythonCard

- [PythonCard](../packages/pythoncard.md) Getting pythoncard to work by editing
  setup.py

### py2exe and Quixote

Quixote is a pythonivc toolkit for web pages which allows one to execute ptl
files using ihooks. You can distribute your web application with medusa or
twisted and hence you can create a web application without IIS or Apache.

I like to distribute my application with py2exe but I can not make py2exe setup
script to recognize that x.ptl is a valid python files. Any idea how to do this?
\- impossible: [Quixote](../packages/quixote.md) HAM20040602

### py2exe and [Matplotlib](../packages/matplotlib.md)

- [Matplotlib](../packages/matplotlib.md) - Fixing and including configuration
  information for this plotting package.

### py2exe and Tix

- [Tix](../packages/tix.md) - Including the Tix DLL and Tcl files to make Tix
  apps work.

### the runtime enviroment

- [Environment](../guides/runtime/environment.md) - Information about the
  environment for the executable

### py2exe and subprocess

- [Subprocess](../guides/runtime/subprocess.md) - Getting subprocess module to
  work with py2exe.

### py2exe and logging module

- [Logging](../packages/logging.md) - Getting the %(filename)s format string
  working in the python logging module.

### py2exe and win32pipe

- [win32pipe](../windows/win32pipe.md) (from pywin32) in a bundle.

### py2exe and Python Eggs

- [Python eggs](../guides/build/python-eggs.md) - A recipe for creating an .exe
  out of eggs

### py2exe and NumPy

- If you're getting *No scipy-style subpackage 'xxx' found in
  c:\\...\\library.zip\\numpy. Ignoring*, try --skip-archive option.

### Fixes

- [Extending example](../troubleshooting/extending-example.md) a "-.zip" is
  missing
- [GUI console output](../guides/runtime/gui-console-output.md) with options
  'windows' still open a console window for errors

## Thoughts

- [Build speed](../guides/optimization/build-speed.md) using psyco to speed up
  code compilation
- [Cross-platform](../development/cross-platform.md)
- Generation of .com and .exe files in one run

---

CategoryHomepage

[link-1]: https://sourceforge.net/projects/py2exe/files/py2exe/0.5.0/
[link-2]: https://mail.python.org/pipermail/python-list/2004-January/283051.html
