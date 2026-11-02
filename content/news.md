# News

## py2exe 0.6.9 released (2008/11/15)

Binaries for Python 2.6 and Python 2.7.

Fixed a modulefinder crash on certain relative imports.

Changed the py2exe\\samples\\singlefile\\gui\\test\_wx.py sample to use the wx
package instead of the old wxPython package.

Copy the manifest, if any, from the 'template' into the targets to ensure
embedded assembly references, as required for python 2.6 based apps, are copied.

Allow each target to specify Vista User Access Control flags. For example,
specifying 'uac\_execution\_info="requireAdministrator"' would force elevation
for the final executable.

## py2exe 0.6.8 released (2008/06/15)

Support for relative imports.

Fix MemoryLoadLibrary to handle loading function addresses by ordinal numbers.
Patch and test by Matthias Miller.

Using the options compressed=1, bundle\_files=3, and zipfile=None at the same
time now works; patch from Alexey Borzenkov.

Allow renaming of single-executable files; patch from Alexey Borzenkov.

Embedding icon resources into the image now works correctly even for ico files
containing multiple images.

pyd files from different packages with the same filename no longer conflict.
Patch from Grant Edwards.

There are new samples for the 'typelibs' support, including the new option of
pre-generating a typelib and specifying the file as an input to py2exe.

The test suite is now included in the source distribution.

## py2exe 0.6.6 released (2006/12/30)

Better support for Python 2.5.

Experimental support for 64-bit builds of Python on win64.

Better ISAPI support.

New samples for ISAPI and COM servers.

Support for new "command-line styles" when building Windows services.

## py2exe 0.6.5 released (2006/03/20)

Fixed modulefinder / mf related bugs introduced in 0.6.4. This
will be most evident when working with things like
win32com.shell and xml.xpath.

Files no longer keep read-only attributes when they are copied
as this was causing problems with the copying of some MS DLLs.

## py2exe 0.6.4 released (2006/02/13)

New skip-archive option which copies the Python bytecode files
directly into the dist directory and subdirectories - no
archive is used.

An experimental new custom-boot-script option which allows a boot
script to be specified (e.g., --custom-boot-script=cbs.py) which can
do things like installing a customized stdout blackhole. See
py2exe's boot\_common.py for examples of what can be done. The custom
boot script is executed during startup of the executable immediately
after boot\_common.py is executed.

Thomas Heller's performance improvements for finding needed
modules.

Mark Hammond's fix for thread-state errors when a py2exe
created executable tries to use a py2exe created COM DLL.

## py2exe 0.6.3 released (2005/10/06)

dll-excludes is now available on the command line and can be used to
exclude msvcr71.dll and w9xpopen.exe.

A bug that caused py2exe to crash when copying extension modules in
packages was fixed.

## py2exe 0.6.2 released (2005/09/07)

Several important bugfixes.

For Python 2.4, MSVCR71.dll is now copied into the dist directory.
This dll cannot be bundled into the executable, sorry.

## py2exe 0.6.1 released (2005/09/05)

Can now create single file executables.
