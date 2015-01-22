## Please edit system and help pages ONLY in the moinmaster wiki! For more
## information, please see MoinMaster:MoinPagesEditorGroup.
##acl MoinPagesEditorGroup:read,write,delete,revert All:read
##master-page:HelpTemplate
##master-date:Unknown-Date
#format wiki
#language en
== Overriding Criteria for Including DLLs ==

When py2exe comes across a DLL file that is required by the
application, it decides whether or not includes the DLL file
in the distribution directory using various criteria.
Generally, it doesn't include DLLs if it thinks they belong to
the "system" rather than the "application".  There is a
function that determines whether a specific DLL is a "system"
DLL or not.  DLLs found in directories like
C:\WINNT\system32\MSVCP71.dll aren't included except for a
special list of exceptions. If you'd like to override the
decision for specific DLL files you can use the hack below
in your setup.py file

=== Example ===
{{{
# setup.py
from distutils.core import setup
import py2exe
import os

old_determine_dll_type = py2exe.dllfinder.DllFinder.determine_dll_type
pack = ("msvcp71.dll", "dwmapi.dll")
def determine_dll_type(self, imagename):
    if os.path.basename(imagename).lower() in pack:
        return "EXT"    
    return old_determine_dll_type(self, imagename)
py2exe.dllfinder.DllFinder.determine_dll_type = determine_dll_type

[remainder of setup.py stuff]
}}}

In the example above, we've over-ridden the function
py2exe.dllfinder.DllFinder.determine_dll_type with our own copy that forces
msvcp71.dll and dwmapi.dll to be considered "application" DLLs
instead of "system" DLLs.  This should cause py2exe to include them in
the application distribution directory.  For any other DLL it returns the
previous default status as returned by the original determine_dll_type function.

=== Disclaimer ===
If you use the above mechanism to trick py2exe into
distributing any "system" DLLs, check to make sure that
you're allowed to distribute those DLLs with your application
or else Steve Ballmer [yadda, yadda, yadda] your cat.
