= Introduction =
[[http://matplotlib.sf.net|MatPlotLib]] is a module to produce nice-looking plots in Python using a wide variety of back-end packages, at least one of which is likely to be available for your system. 

== Data Files ==
matplotlib requires some data files:

{{{
#!python
import matplotlib
...
setup(
    ...
    data_files=matplotlib.get_py2exe_datafiles(),
)
}}}

(This works for recent versions of matplotlib; for older versions, see this page's history for alternative approaches.)

== Backends ==

matplotlib has many backends; if all of them get included, your distribution could get large. You might want to do something like:

{{{
#!python
setup(options={'py2exe': { ...
                'excludes': ['_gtkagg', '_tkagg'],
}})
}}}

If you omit a backend, you must make sure it isn't the default - for example if you package the wx backend and not Tcl/Tk. The default backend is configured in mpl-data/matplotlib.conf. You can override the configuration in your program by doing, for example:
{{{
#!python
import matplotlib
matplotlib.use('wxagg') # overrule configuration
import pylab
}}}


== Other things you may need ==

Below are snippets that others have, at one time or another, needed to get matplotlib working.

=== Includes and excludes ===
{{{
#!python
opts = {
    'py2exe': { 'includes': 'matplotlib.numerix.random_array',
                'excludes': ['_gtkagg', '_tkagg'],
                'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                 'libgobject-2.0-0.dll']
              }
       }
}}}

=== Data Files ===
{{{
#!python
from distutils.core import setup
import py2exe

from distutils.filelist import findall
import os
import matplotlib
matplotlibdatadir = matplotlib.get_data_path()
matplotlibdata = findall(matplotlibdatadir)
matplotlibdata_files = []
for f in matplotlibdata:
    dirname = os.path.join('matplotlibdata', f[len(matplotlibdatadir)+1:])
    matplotlibdata_files.append((os.path.split(dirname)[0], [f]))


setup(
    console=['test.py'],
    options={
             'py2exe': {
                        'packages' : ['matplotlib', 'pytz'],
                       }
            },
    data_files=matplotlibdata_files
)
}}}

=== Setup.py using py2exe with Python2.5 and matplotlib 0.91.2 ===
--~~~~ In this example, a simple program was created where a matplotlib figure canvas is placed in a PyQt child window.  In order to compile it with py2exe and matplotlib 0.91.2 with Python 2.5, it is necessary to include the necessary modules and then add the data files properly.  On this system, the matplotlib was installed to the folder Python25\Lib\site-packages.  Within the matplotlib folder, the matplotlib-data is saved in mpl-data.

Using the above methods would result in the classic "RuntimeError: Could not find the matplotlib data files" error.  Furthermore, using the method with data_files = matplotlib.get_py2exe_datafiles(), py2exe returns an error saying that 'split' is not a valid method for this object.  Another problem when using glob, the and a * is located in the argument, glob will search for everything, including folders.  Doing this will give you an error when compiling saying that 'fonts' is not a file.  So you need to add the contents from mpl-data\fonts and mpl-data\images individually.

Ensure that the first entry in the tuple in the list 'data_files' is matches the actual matplotlib data folder; in this case 'mpl-data' (and then later mpl-data\fonts and mpl-data\images).  Also, the file matplotlibrc file is not returned by 'glob' so it is also added manually.

This is modified from the above setup.py under ''Special content for setup.py to use matplotlib''

{{{
#!python
# Used successfully in Python2.5 with matplotlib 0.91.2 and PyQt4 (and Qt 4.3.3)
from distutils.core import setup
import py2exe

# We need to import the glob module to search for all files.
import glob

# We need to exclude matplotlib backends not being used by this executable.  You may find
# that you need different excludes to create a working executable with your chosen backend.
# We also need to include include various numerix libraries that the other functions call.

opts = {
    'py2exe': { "includes" : ["sip", "PyQt4._qt", "matplotlib.backends",  "matplotlib.backends.backend_qt4agg",
                               "matplotlib.figure","pylab", "numpy", "matplotlib.numerix.fft",
                               "matplotlib.numerix.linear_algebra", "matplotlib.numerix.random_array",
                               "matplotlib.backends.backend_tkagg"],
                'excludes': ['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg',
                             '_fltkagg', '_gtk', '_gtkcairo', ],
                'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                 'libgobject-2.0-0.dll']
              }
       }

# Save matplotlib-data to mpl-data ( It is located in the matplotlib\mpl-data
# folder and the compiled programs will look for it in \mpl-data
# note: using matplotlib.get_mpldata_info
data_files = [(r'mpl-data', glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\*.*')),
                    # Because matplotlibrc does not have an extension, glob does not find it (at least I think that's why)
                    # So add it manually here:
                  (r'mpl-data', [r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
                  (r'mpl-data\images',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
                  (r'mpl-data\fonts',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\fonts\*.*'))]

# for console program use 'console = [{"script" : "scriptname.py"}]
setup(windows=[{"script" : "scriptname.py"}], options=opts,   data_files=data_files)
}}}
= Updating _sort confusion =
If you're using numarray and numpy together, be aware that they both have a _sort, and py2exe gets them confused. After py2exe creates the dist directotry, copy numpy/core/_sort.pyd and numarray/sort.pyd to their respective locations in the dist.

If you get an error that numarray module has no functionDict in numarraycore.py at line 176, then you'll know that py2exe confused the _sort modules that are in both numpy and numarray and need to do this step.

= MPL datafiles etc with Python 2.5 and MPL 0.99 =
Using matplotlib.get_py2exe_datafiles() helps to make this really easy now.

Following is a setup.py for the MPL example "embedding_in_wx2.py" (you should comment the wxversion check in that file or make it conditional on sys.frozen).

{{{
from distutils.core import setup
import py2exe

# Remove the build folder, a bit slower but ensures that build contains the latest
import shutil
shutil.rmtree("build", ignore_errors=True)

# my setup.py is based on one generated with gui2exe, so data_files is done a bit differently
data_files = []
includes = []
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter', 'pydoc', 'doctest', 'test', 'sqlite3'
            ]
packages = ['pytz']
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll']
icon_resources = []
bitmap_resources = []
other_resources = []

# add the mpl mpl-data folder and rc file
import matplotlib as mpl
data_files += mpl.get_py2exe_datafiles()

setup(
    windows=['embedding_in_wx2.py'],
                          # compressed and optimize reduce the size
    options = {"py2exe": {"compressed": 2, 
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          # using 2 to reduce number of files in dist folder
                          # using 1 is not recommended as it often does not work
                          "bundle_files": 2,
                          "dist_dir": 'dist',
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },

    # using zipfile to reduce number of files in dist
    zipfile = r'lib\library.zip',

    data_files=data_files
)
}}}

In 0.99 there is a problem with some of the documentation strings, which shows up if you use "optimize=1or2", the work around is quite easy and according to the MPL list this is fixed in trunk.

This kind of code:
{{{
psd.__doc__ = psd.__doc__ % kwdocd
}}}

Causes a TypeError exception if one uses ""optimize": 1or2," in ones setup.py.

My work around is to change that type of code to:
{{{
if psd.__doc__ is not None:
    psd.__doc__ = psd.__doc__ % kwdocd
else:
    psd.__doc__ = ""
}}}
I got this problem only with mpl/mlab.py, in which four lines need to be changed.

Another issue I found if you need to use the backend_wx, it does a version check for wxPython 2.8 which always fails in the py2exe version, my work around is to add "if not hasattr(sys, 'frozen'):" at line 113 of backend_wx.py and indent the lines 114 to 131.  I will report this to the mpl list and they will hopefully fix this too.
