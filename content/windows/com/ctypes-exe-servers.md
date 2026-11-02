# ctypes EXE servers

Use attribute **windows** or **console** of method **setup** to create a com exe
server.
Unlike the case with win32com, with ctypes.com only a exe server will be
created.
Also see: [win32com servers](win32com-servers.md) &amp;
[ctypes DLL servers](ctypes-dll-servers.md)

You can define and instantiate a **Target** class to explicitly add
version info resources that get attached to the file as metadata.

file **setup.py** would look something like this:

```python
# This is the distutils script for creating a Python-based com exe
# server using ctypes.com.  This script should be run like this:
#
#  % python setup.py py2exe
#
# After you run this (from this directory) you will find two directories here:
# "build" and "dist".  The .exe file in dist is what you are looking for.
##############################################################################

from distutils.core import setup
import py2exe
import sys

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the version info resources (Properties -- Version)
        self.version = "0.0.1"
        self.company_name = "my company"
        self.copyright = "© 2006, my company"
        self.name = "my com server name"

my_com_server_target = Target(
    description = "my com server",
    # use filename for ctypes.com exe server
    script = "dir\my_com_server.py",
    # dest_base specifies basename of the exe file (should match setup name)
    dest_base = "my_com_server",
    # the following line embeds the typelib within the exe
    other_resources = [("TYPELIB", 1, open(r"dir\my_com_server.tlb", "rb").read())],
    # we only want the local (exe) server
    create_dll = False
    )

setup(
    name="my_com_server",
    # the following two parameters embed support files within exe file
    options={"py2exe": {"bundle_files": 1, }},
    zipfile=None,
    version="0.0.1",
    description="my com server",
    # author, maintainer, contact go here:
    author="First Last",
    author_email="some_name@some_company.com",
    packages=["dir"],
    windows=[my_com_server_target]
    )
```
