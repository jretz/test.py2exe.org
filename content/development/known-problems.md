Problems in '''py2exe 0.6.6''' that should be fixed:

 . - '''Error reporting in MemoryLoadLibrary must be improved.'''  When MemoryLoadLibrary fails because it cannot find a required DLL (for example), it is impossible to diagnose the problem.  This is from a post to the py2exe-users mailing list:
 {{{
Traceback (most recent call last):
  File "Wk2000.py", line 3, in ?
  File "zipextimporter.pyo", line 82, in load_module
  File "wx\__init__.pyo", line 45, in ?
  File "zipextimporter.pyo", line 82, in load_module
  File "wx\_core.pyo", line 4, in ?
  File "zipextimporter.pyo", line 98, in load_module
ImportError: MemoryLoadLibrary failed loading wx\_core_.pyd
 }}}
 ''This error occur when no msvcp71.dll found - add this dll to program or windows/system32 director [Sep]''
 . - '''When the python module archive is compressed and appended to the exe but bundle_files>2 then zlib cannot be found''' When the archive is a separate file and it is compressed zlib.pyd is correctly prepended to the archive, but when the archive is appended to the exe zlib.pyd is only added as a resource when bundle_files<3. This is a mistake. It worked under py2exe 0.6.5 because zlib.pyd which wasn't bundled could be loaded straight from the file system, but in 0.6.6 the path was "fixed" to remove the current directory from the path so zlib.pyd can't be loaded directly and the loader script is in the archive we can't uncompress. You'll get a traceback like this:
 {{{
Traceback (most recent call last):
  File "c:\Panda3D-1.3.2\python\lib\site-packages\py2exe\boot_common.py", line 92, in ?
    import linecache
zipimport.ZipImportError: can't decompress data; zlib not available
Traceback (most recent call last):
  File "Example.py", line 1, in ?
zipimport.ZipImportError: can't decompress data; zlib not available
 }}}
 I wrote [[http://sparkyb.net/temp/py2exe-0.6.6-zlib-resource.patch|this patch]] which seems to fix it.
