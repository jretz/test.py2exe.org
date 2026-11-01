If your programs alters Python import mechanism somehow (like many applications with plugins and extensions) you may run into problems with py2exe. This page is dedicated to explain the reasons for these problems and how to solve them. If you have an experience to share, please add your story here.

=== Check that zipextimporter works on your system ===
zipextimporter is the starting component of py2exe that may cause problems. To debug it you will need _memimporter.pyd binary module. These modules can be found in binary py2exe distributions for your Python version (I unpack .exe distribution with 7Zip). zipextimporter contains the following script to help with debugging using standard _socket.pyd module. Wrap _socket.pyd from your Python version into ''lib.zip'' and use the script to see that zipextimporter works ok.

{{{
#!python
import zipextimporter
zipextimporter.install()

import sys
sys.path.insert(0, "lib.zip")

import _socket
print _socket
# <module '_socket' from 'lib.zip\_socket.pyd'>
print _socket.__file__
# 'lib.zip\\_socket.pyd'
print _socket.__loader__
# <ZipExtensionImporter object 'lib.zip'>
# Reloading also works correctly:
print _socket is reload(_socket)
# True
}}}

=== Debugging compiled .exe with PY2EXE_VERBOSE ===
PY2EXE_VERBOSE is an environment variable that is understood by compiled .exe module. By setting this variable to 1 or 2 you can get verbose (or very verbose) log actions done by py2exe importer.

To get this debug log while using zipextimporter.py directly, you will need to insert this monkeypatching hack at the beginning of your test script:
{{{
#!python
import zipextimporter
zipextimporter.install()

import _memimporter
_memimporter.get_verbose_flag = lambda: 2

# ...
}}}

=== Use debug version of zipextimporter.py with very verbose output ===
Attached [[attachment:zipextimporter-debug-0.6.9.py]] version understands value 3 of verbose flag of memimporter and can give a lot of useful output. Hope some parts can be committed to py2exe.
