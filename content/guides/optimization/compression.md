# Compression

## Something great

Within samples/extending, Thomas Heller gives a
[py2exe](../../getting-started/overview.md) setup.py script which automagically
calls [InnoSetup](http://www.jrsoftware.org/isinfo.php) to create a great
looking (and perfectly working) Windows-Installer. Yes, really, ONE setup.exe is
created which contains ALL stuff to have a readily installable Software out of
your product.

## also large

I program using wxPython. A great library, a large library.

```output
2.240.512 wxc.pyd 
3.416.064 wxmsw24uh.dll
```

Two modules you cannnot skip. In addition there is as allways

```output
974.915 python23.dll
```

giving more than 6 Megabytes with no line of code written

In total:

```output
28 Datei(en)      9.549.525 Bytes  (in lib)
```

and

```output
2 Datei(en)      1.011.779 Bytes   (in prog)
```

summing up to 10.5 Megabyte ... not much with DSL, but... shocking, isn't it?

## get it smaller

In the standard configuration [InnoSetup](http://www.jrsoftware.org/isinfo.php)
compressed it down to around 6.5 Megabyte.

I changed the setup.py to contain

```python
print >> ofi, r"[Setup]"
print >> ofi, r"AppName=%s" % self.name
print >> ofi, r"AppVerName=%s %s" % (self.name, self.version)
print >> ofi, r"DefaultDirName={pf}\%s" % self.name
print >> ofi, r"DefaultGroupName=%s" % self.name
print >> ofi, r"Compression=bzip" 
print >> ofi
```

... the special line is

```python
print >> ofi, r"Compression=bzip" 
```

## the result

```output
4.335.283 setup.exe 
```

Quite an OK download ... and I use ZODB and Elementtree and pythoncom and and
and....

## Remarks

- I ([MGr](http://videocapture.sourceforge.net/)) get for my application (which
  uses wxWindows) even smaller files when using 7-zip instead of bzip. To use
  7-zip one has to specify "Compression=none" in the generated installer script
  (\*.iss) and then manually load the script into
  [ISTool](http://www.istool.org/), which is a front end to Inno Setup. Clicking
  at the 'Options' button and selecting '7-zip' in the compression combo box
  does the trick.

```output
7.208 kB  uncompressed
2.886 kB  zip
2.677 kB  bzip
2.160 kB  7-zip
```

The previous comparison shows, that 7-zip results by far in the smallest
installer size. An additional benefit of using 7-zip is the fast installation.
When using bzip, the files are decompressed in the last step of the installation
process, right then when the files are written to the program folder. Since bzip
is computationally quite intensive, the progress bar fills not extremely fast.
When using 7-zip, there is a short decompression when starting the installer,
but the installation process afterwards it fast as lightning, because of
"Compression=none" :) .

Addition:

Innosetup 4.2 has 7z "LZMA" compression included. Just use

```python
print >> ofi, r"Compression=lzma/max" 
```

HAM2005-05-20

## 7ZIP and UPX

Repacking the "library.zip" with [7-ZIP](http://www.7-zip.org/) saving 357KB
(577KB original to 220KB 7ZIP compressed).
Note: it requires "import zlib" in your source file to allow unzipping
operations.

Using [UPX](http://upx.sourceforge.net/) the executable packer to compress
\*.pyd, \*.dll and \*.exe Files:

Example: \_sre.pyd, \_winreg.pyd, python23.dll, unicodedata.pyd, w9xpopen.exe,
zlib.pyd 1516,2KB original to 584KB compressed)

Everything together: Original Size: 2093,2 compressed: 804KB !!!

A short Windows Batch-File to automate (see
[Batch builds](../build/batch-builds.md)):

```bat
7z.exe -aoa x library.zip -olibrary\
del library.zip

cd library\
7z.exe a -tzip -mx9 ..\library.zip -r
cd..
rd library /s /q

upx.exe --best *.*
```

## Automatically UPXing extension modules/dlls

While converting over from prior use of the Installer package, I missed its
ability to automatically UPX binary modules as they were included in the
distribution. So this example creates a custom command class based on py2exe
that performs the UPX as part of the file copy process into the distribution
directory. The one difference compared to Installer is that it doesn't currently
keep a cache of UPXed files, although it could easily enough be extended to do
that.

Note that as designed I believe it will UPX any dll/pyd file copied over, even
if they are part of the data files for the application. But since anything
packaged up with py2exe is going to be running independently and unlikely to
need to share any DLLs with other applications, there's little harm in UPXing
anything in sight.

The class below is a portion of a py2exe-subclass command class that I use that
does the following, based on a new "upx" configuration value:

- Compress (using upx) any dll or pyd file that is copied into the distribution
  directory. Since it does this at copy time, you only take the hit of upx
  whenever the file is updated (or you clean out the dist directory).
- Deals with the fact that you have to postpone UPXing the main python##.dll
  file until py2exe has a chance to fix it's version identification, and that
  you shouldn't re-patch the file once it's been UPXed.

This command class was written with py2exe 0.5.4.

```python2
from distutils.core import setup
from py2exe.build_exe import py2exe

#--------------------------------------------------------------------------
#
# Define our own command class based on py2exe so we can perform some
# customizations, and in particular support UPXing the binary files.
#
#--------------------------------------------------------------------------

class Py2exe(py2exe):

    def initialize_options(self):
        # Add a new "upx" option for compression with upx
        py2exe.initialize_options(self)
        self.upx = 0

    def copy_file(self, *args, **kwargs):
        # Override to UPX copied binaries.
        (fname, copied) = result = py2exe.copy_file(self, *args, **kwargs)

        basename = os.path.basename(fname)
        if (copied and self.upx and
            (basename[:6]+basename[-4:]).lower() != 'python.dll' and
            fname[-4:].lower() in ('.pyd', '.dll')):
            os.system('upx --best "%s"' % os.path.normpath(fname))
        return result

    def patch_python_dll_winver(self, dll_name, new_winver=None):
        # Override this to first check if the file is upx'd and skip if so
        if not self.dry_run:
            if not os.system('upx -qt "%s" >nul' % dll_name):
                if self.verbose:
                    print "Skipping setting sys.winver for '%s' (UPX'd)" % \
                          dll_name
            else:
                py2exe.patch_python_dll_winver(self, dll_name, new_winver)
                # We UPX this one file here rather than in copy_file so
                # the version adjustment can be successful
                if self.upx:
                    os.system('upx --best "%s"' % os.path.normpath(dll_name))
```

This class would then be used in your main setup() call as:

```python2
setup(...
      cmdclass = {'py2exe': Py2exe}
      ...
      )
```

For a simple project of mine that is built as a Windows service, this made the
binaries in the installation take about a third of the size they would otherwise
have needed, which was about half the size of the overall project. When built
with UPX it was just under a MB, with the UPXing saving me about a MB on the
binaries:

```output
        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
    979005 ->    370176   37.81%    win32/pe     python23.dll
     49212 ->     16896   34.33%    win32/pe     support/_socket.pyd
     57401 ->     18432   32.11%    win32/pe     support/_sre.pyd
     36864 ->     11264   30.55%    win32/pe     support/_winreg.pyd
     45117 ->     17408   38.58%    win32/pe     support/datetime.pyd
     24576 ->      6144   25.00%    win32/pe     support/perfmon.pyd
     20539 ->      5120   24.92%    win32/pe     support/select.pyd
     36864 ->     10752   29.16%    win32/pe     support/servicemanager.pyd
     69632 ->     21504   30.88%    win32/pe     support/win32api.pyd
     24576 ->      5632   22.91%    win32/pe     support/win32event.pyd
     77824 ->     20992   26.97%    win32/pe     support/win32file.pyd
     40960 ->     11776   28.75%    win32/pe     support/win32service.pyd
     61497 ->     23552   38.29%    win32/pe     support/zlib.pyd
     94208 ->     40448   42.93%    win32/pe     support/pywintypes23.dll
   --------------------   ------   -----------   -----------
   1618275 ->    580096   35.84%                 [ 14 files ]
```

For a much larger project (involving wxPython, Twisted, etc..), the binaries
were again about a third of the size, but in this case ended up saving me over
7.5MB of space. The overall project distribution (UPXed) is about 15MB:

```output
        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
    979005 ->    370176   37.81%    win32/pe     python23.dll
      6656 ->      4096   61.53%    win32/pe     support/_c_urlarg.pyd
     73728 ->     26624   36.11%    win32/pe     support/_ctypes.pyd
    280064 ->    133120   47.53%    win32/pe     support/_imaging.pyd
    170496 ->     86016   50.45%    win32/pe     support/_imagingft.pyd
     49212 ->     16896   34.33%    win32/pe     support/_socket.pyd
     27648 ->      9728   35.18%    win32/pe     support/_speedups.pyd
     57401 ->     18432   32.11%    win32/pe     support/_sre.pyd
    495616 ->    197120   39.77%    win32/pe     support/_ssl.pyd
     36864 ->     11264   30.55%    win32/pe     support/_winreg.pyd
     15360 ->      7680   50.00%    win32/pe     support/cBanana.pyd
     45117 ->     17408   38.58%    win32/pe     support/datetime.pyd
    196608 ->     36352   18.49%    win32/pe     support/htmlc.pyd
     24576 ->      6144   25.00%    win32/pe     support/mmap.pyd
     61440 ->     17920   29.16%    win32/pe     support/mxDateTime.pyd
    135228 ->     47616   35.21%    win32/pe     support/pyexpat.pyd
     20539 ->      5120   24.92%    win32/pe     support/select.pyd
     32768 ->      8704   26.56%    win32/pe     support/sha256.pyd
    405504 ->    171008   42.17%    win32/pe     support/unicodedata.pyd
     69632 ->     21504   30.88%    win32/pe     support/win32api.pyd
     24576 ->      5632   22.91%    win32/pe     support/win32event.pyd
     77824 ->     20992   26.97%    win32/pe     support/win32file.pyd
     36864 ->     10752   29.16%    win32/pe     support/win32process.pyd
     20480 ->      5120   25.00%    win32/pe     support/win32trace.pyd
    655360 ->    168448   25.70%    win32/pe     support/win32ui.pyd
     32768 ->      9216   28.12%    win32/pe     support/win32uiole.pyd
   2240512 ->    367616   16.40%    win32/pe     support/wxc.pyd
     61497 ->     23552   38.29%    win32/pe     support/zlib.pyd
   1712128 ->    602112   35.16%    win32/pe     support/chartdir.dll
     69632 ->     27136   38.97%    win32/pe     support/pychartdir23.dll
    315392 ->    105472   33.44%    win32/pe     support/pythoncom23.dll
     94208 ->     40448   42.93%    win32/pe     support/pywintypes23.dll
   3416064 ->   1494016   43.73%    win32/pe     support/wxmsw24uh.dll
   --------------------   ------   -----------   -----------
  11940767 ->   4093440   34.28%                 [ 33 files ]
```

-- David Bolen
