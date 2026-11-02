# Embedded resources

## How to add custom data into the executable?

Sometimes it is very useful to be able to insert binary data into the final
executable. The most casual use case is to insert version strings into the
binary without having to modify the main script source code.

This is done very simply by inserting a custom named resource into the
executable such as shown in the example below.
In this case, I chose "VERSIONTAG" but you are free to use any unicode string.

### Example

```python2
from distutils.core import setup

myrevisionstring="prog internal rev 1.0"
setup(windows=[{'script': "prog.py", 
                'other_resources': [(u"VERSIONTAG",1,myrevisionstring)],
                             'icon_resources': [(1,'prog.ico')]
               }],
               zipfile = r"subdir\modules.dat",
               name="My Program",
               version="1.0",
     )
```

## More fun with resources

For all the following, you must download and install the other excellemt module
from ThomasHeller: [ctypes](http://starship.python.net/crew/theller/ctypes/)

First you can define the following code in a separate module (winrsc.py for
example)

```python2
from ctypes import *

def GetModuleHandle(filename=None):
    h=windll.kernel32.GetModuleHandleW(filename)
    if not h:
        raise WinError()
    return h

def FindResource(typersc,idrsc,c_restype=c_char,filename=None):
    if type(idrsc)is int:
        idrsc=u'#%d'%idrsc
    if type(typersc) is int:
        typersc=u'#%d'%typersc
    hmod=GetModuleHandle(filename)
    hrsc=windll.kernel32.FindResourceW(hmod,typersc,idrsc)
    if not hrsc:
        raise WinError()
    hglobal=windll.kernel32.LoadResource(hmod,hrsc)
    if not hglobal:
        raise WinError()
    windll.kernel32.LockResource.restype=POINTER(c_restype)
    return windll.kernel32.LockResource(hglobal)[0]

```

Then in another module, you create some kind of data structure. privdata.py

```python2
from ctypes import *

class MyPrivateInfo(Structure):
    _fields_ = [ ("ver",c_int),("debug",c_int),("copyright_info",c_char*100) ]
    def get_buffer(self):
        return cast(pointer(self),POINTER(c_char*sizeof(self)))[0].raw


```

And in your setup you can do.

```python2
import privdata

setup(windows=[{'script': "prog.py", 
                'other_resources': [(u"PRIVTAG",1,privdata.MyPrivateInfo(100,100,"My Copyright notice").get_buffer()],
                             'icon_resources': [(1,'prog.ico')]
               }],
               zipfile = r"subdir\modules.dat",
               name="My Program",
               version="1.0",
     )

```

This should insert a resource with the info that you give to the constructor of
your private object.

Finally, at runtime in your frozen executable you can do:

```python2
import privdata
import winrsc
try:
    someinfo=winrsc.FindResource("PRIVTAG",1,c_restype=privdata.MyPrivateInfo)
except Exception,e:
    someinfo=None

if someinfo:
    print someinfo.ver
    print someinfo.copyright_info
```

This is quite useful if you want to have a single executable but different
behaviour depending on a flag. For example, if a debug flag is set, you can
choose to log all errors to the console instead of ignoring them etc.
