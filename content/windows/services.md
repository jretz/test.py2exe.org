# Windows services

You can build Windows NT services by passing a `service` keyword
argument to the `setup` function, the value must be a list of Python
module names containing a service class (identified by the `_svc_name_`
attribute):

```python2
# setup.py
from distutils.core import setup
import py2exe

setup(service=["MyService"])
```

Optionally, you can specify a `cmdline_style` attribute to py2exe, with
valid values being `py2exe` (the default), `pywin32` or `custom`. `py2exe`
specifies the traditional command-line always supported by py2exe. `pywin32`
supports the exact same command-line arguments as pywin32 supports (ie, the
same arguments supported when running the service from the .py file.)
`custom` means that your module is expected to provide a `HandleCommandLine`
function which is responsible for all command-line handling.

The built service executables are able to install and remove
themselves by calling them with certain command line flags, run the
exe with the `-help` argument to find out more.

## Making services more like regular win32 apps

From <https://sourceforge.net/p/py2exe/mailman/message/6938994/>, update
your setup.py to look something like this:

```python2
myservice = Target(
    # used for the versioninfo resource
    description = "A sample Windows NT service",
    # what to build. For a service, the module name (not the
    # filename) must be specified!
    modules = ["MyService"],
    cmdline_style='pywin32',
    )

setup(
    service = [myservice],
    )
```

See `samples\advanced\setup.py` for more details.

**Note**: using an object for `setup()` is a py2exe extension of
distutils

The standard win32 commands for `HandleCommandLine()`:

- install
- start
- debug
- stop
- remove

Without the `cmdline_style` parameter, you get this output from running your
service in CMD:

```py2tb
Services are supposed to be run by the system after they have been installed.
These command line options are available for (de)installation:
        -help
        -install
        -remove
        -auto
        -disabled
        -interactive
        -user: <arg>
        -password: <arg>
Connecting to the Service Control Manager
Traceback (most recent call last):
  File "boot_service.py", line 173, in ?
pywintypes.error: (1063, 'StartServiceCtrlDispatcher', 'The service process could not connect to the service controller.')
```

In 'py2exe 0.9.2.2 for Python 3.3 and later' 'cmdline\_style' is not passed to
the compile system, while it is defined in the setup-script.

Workaround/Fix:

```diff
<Python PATH>\Lib\site-packages\py2exe\runtime.py: line 561
-                compile("cmdline_style = 'py2exe'; service_module_names = %r" % (target.modules,),
+                compile("cmdline_style = '%s'"%(getattr(target,"cmdline_style","py2exe")) + "; service_module_names = %r" % (target.modules,),
```

## Things that can go wrong with py2exe and services

within demos/advanced there is an example to create windows services with
py2exe. It works quite out of the box.

Difficulties arise later on - as soon as you wanna do something REAL with that
service.

### Error Message

```py2tb
Python could not import the service's module
  File "C:\ham\jds\syncservice.py", line 21, in ?
    import transinhalte
  File "C:\ham\jds\transinhalte.py", line 17, in ?
    import unite
  File "C:\ham\jds\unite.py", line 9, in ?
    import version
exceptions.ImportError: dynamic module does not define init function (initversion)
```

yours might be different ... what went wrong????

Everything worked fine as long as I was running that service within debug mode.
Then, starting it up as "real service", this error appeared.

[a Mail of Gerald Haering][link-1] showed me the light:
when a service is started, all paths are TOTALLY DIFFERENT ANIMALS then in any
other running state of python...
so, the service tried to load version.dll, which is something that comes within
windows/system32, and of course has NO Python init-code.

### Solution

Make sure that NONE of your Python module names conflicts with ANY of the
windows system dll names

[link-1]: https://groups.google.com/g/comp.lang.python/c/VbJrJ1_OfqQ/m/FDLYnPlRcqwJ
