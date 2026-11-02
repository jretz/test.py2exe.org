# Options

## What you need to understand about Distutils&#58;

The Distutils module is part of the standard python distribution. Distutils is
used by python module developers to package and distribute new modules. The
setup syntax py2exe uses is inherited from distutils. (If you choose the default
Windows installation for python, distutils can be found at: C:/Program
Files/Python##/Lib/distutils/). The setup function of Distutil
[recognizes specific keywords][link-1], which are also available when running
py2exe. The following is a list of some more useful distutils keywords

| **keyword** | **description** |
| --- | --- |
| [Data files](data-files.md) | list of "data" files that you are going to need to run your executable such as .pngs, .jpgs |

## Py2exe extends Distutils setup keywords

In addition to the standard distutils setup keywords, the following py2exe
keywords specify what and how to build.

| **keyword** | **description** |
| --- | --- |
| console | list of scripts to convert into console exes |
| windows | list of scripts to convert into GUI exes |
| service | list of module names containing win32 service classes |
| com\_server | list of module names containing com server classes |
| ctypes\_com\_server | list of module names containing com server classes |
| zipfile | name of shared zipfile to generate; may specify a subdirectory; defaults to 'library.zip'. If `zipfile` is set to `None`, the files will be bundled within the executable instead of 'library.zip'. |
| options | dictionary { "py2exe": { *"opt1": val1, "opt2": val2, ...* } } |

## The options dictionary of py2exe

The option keyword takes the following set of dictionary key: value pairs. The
dictionary "key" names and the "value" types are listed in the table below.

| **key** | **value** |
| --- | --- |
| unbuffered | if true, use unbuffered binary stdout and stderr |
| optimize | string or int of optimization level (0, 1, or 2) 0 = don’t optimize (generate .pyc) 1 = normal optimization (like python -O) 2 = extra optimization (like python -OO) See <http://docs.python.org/distutils/apiref.html#module-distutils.util> for more info. |
| includes | list of module names to include |
| packages | list of packages to include with subpackages |
| ignores | list of modules to ignore if they are not found |
| excludes | list of module names to exclude |
| dll\_excludes | list of dlls to exclude |
| dist\_dir | directory in which to build the final files |
| typelibs | list of gen\_py generated typelibs to include |
| compressed | (boolean) create a compressed zipfile |
| xref | (boolean) create and show a module cross reference |
| bundle\_files | bundle dlls in the zipfile or the exe. Valid values for `bundle_files` are: 3 = don't bundle (default) 2 = bundle everything but the Python interpreter 1 = bundle everything, including the Python interpreter |
| skip\_archive | (boolean) do not place Python bytecode files in an archive, put them directly in the file system |
| ascii | (boolean) do not automatically include encodings and codecs |
| custom-boot-script | Python file that will be run when setting up the runtime environment |

Example:

```python2
setup(
        windows=['trypyglet.py'],
        options={
                "py2exe":{
                        "unbuffered": True,
                        "optimize": 2,
                        "excludes": ["email"]
                }
        }
)
```

For more information enter the following at the python command line:

```pycon
>>> from distutils.core import setup
>>> help(setup)
```

[link-1]: http://docs.python.org/dist/module-distutils.core.html
