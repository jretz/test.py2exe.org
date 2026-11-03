# PyGTK

create your handytool.py:

```python2
import sys
import pygtk
if not sys.platform == 'win32':
    pygtk.require('2.0')
import gtk

from mainwindow import MainWindow

if __name__ == '__main__':
    # enable threading
    gtk.threads_init()
    gtk.threads_enter()

    # create the main window
    myapp = MainWindow()

    # start the program loop
    gtk.main()

    # cleanup
    gtk.threads_leave()
```

create your setup.py file:

```python2
from distutils.core import setup
import py2exe
import os

# Find GTK+ installation path
__import__('gtk')
m = sys.modules['gtk']
gtk_base_path = m.__path__[0]

setup(
    name = 'handytool',
    description = 'Some handy tool',
    version = '1.0',

    windows = [
                  {
                      'script': 'handytool.py',
                      'icon_resources': [(1, "handytool.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings',
                      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
                      'includes': 'cairo, pango, pangocairo, atk, gobject, gio, gtk.keysyms, rsvg',
                  }
              },

    data_files=[
                   'handytool.glade',
                   'readme.txt',
                   # If using GTK+'s built in SVG support, uncomment these
                   #os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'gdk-pixbuf-query-loaders.exe'),
                   #os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'libxml2-2.dll'),
               ]
)
```

run setup.py py2exe. You'll get a warning:

```python2
The following modules appear to be missing
['gdk', 'ltihooks']
```

Ignore it ;)

Once that's done, **you'll need to copy the etc, lib and share directories from
your GTK+ install (*not* the pygtk install) to the dist dir py2exe created.**
Optionaly, you can clean the share\\locale dir to include only the locales you
need for GTK+. Same thing for share\\themes (I left both Default and
MS-Windows).

- it seems that from lib/ only all the \*.dlls in the subtree are needed, and
  from share/ only themes/ and locale/. saves lots of space

If you are using
[GtkBuilder][link-3]
and later versions of GTK+ and PyGTK, you may get the following error message:

```py2tb
Y:\my_handytool\dist\library.zip\gtk\_gtk.py:10: RuntimeWarning: tp_compare didn't return -1 or -2 for exception
ImportError: could not import gio
ImportError: could not import gio
Traceback (most recent call last):
  File "my_handytool.py", line 88, in <module>
  File "my_handytool.py", line 75, in __init__
AttributeError: 'module' object has no attribute 'Builder'
```

This issue can be resolved by [adding the 'gio' module][link-1] to the py2exe
includes option in the setup.py file:

```diff
--- setup.py.org        2010-11-13 22:35:20.000000000 +0100
+++ setup.py    2010-11-13 20:26:02.000000000 +0100
@@ -14,7 +14,7 @@
     options = {
         'py2exe': {
             'dist_dir':'dist',
-            'includes': 'cairo, pango, pangocairo, atk, gobject',
+            'includes': 'cairo, pango, pangocairo, atk, gobject, gio',
             }
         },
```

If you are using kiwi, you will also have to copy the *contents* of the (*path
to python*)/share/kiwi directory (and (*path to python*)/share/gazpacho, if you
used gazpacho) to the dist dir. And you will have to create an empty 'kiwi'
directory in the dist/pixmaps directory that you just copied there. (note: I
have not tested kiwi with the Innosetup installer, but if you try it and it
works edit this page and remove this note :) )

Note you'll want to set the working directory (Start in:) for any shortcut you
create to the application directory containing the executable.

(Optional) an Innosetup .iss file to create an installer for handytool:

```ini
[Setup]
AppName=handytool
AppVerName=handytool 1.0
AppPublisher=me
AppPublisherURL=http://www.localhost.me
DefaultDirName={pf}\handytool
DefaultGroupName=handytool
DisableProgramGroupPage=true
OutputBaseFilename=setup
Compression=lzma
SolidCompression=true
AllowUNCPath=false
VersionInfoVersion=1.0
VersionInfoCompany=me inc
VersionInfoDescription=handytool
PrivilegeRequired=admin

[Dirs]
Name: {app}; Flags: uninsalwaysuninstall;

[Files]
Source: dist\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: {group}\handytool; Filename: {app}\handytool.exe; WorkingDir: {app}

[Run]
; If you are using GTK's built-in SVG support, uncomment the following line.
;Filename: {cmd}; WorkingDir: "{app}"; Parameters: "/C gdk-pixbuf-query-loaders.exe > lib/gdk-pixbuf-2.0/2.10.0/loaders.cache"; Description: "GDK Pixbuf Loader Cache Update"; Flags: nowait runhidden
Filename: {app}\handytool.exe; Description: {cm:LaunchProgram,handytool}; Flags: nowait postinstall skipifsilent
```

This Recipe has been tested with:

- [Windows XP SP2 and Windows 7 Ultimate x64](http://www.microsoft.com/)
- [Python 2.4.3 and Python 2.7.2](http://www.python.org/download/)
- [gtk-win32 2.8.14-rc1][link-4]
- [pycairo 1.0.2-1][link-5]
- [pygtk 2.8.4-1 and 2.24.8][link-2]
- [kiwi 1.9.20](https://github.com/stoq/kiwi) *optional*
- [py2exe 0.6.5 and 0.6.9](../index.md)
- [Inno Setup 5.1.6 and 5.4.3](https://jrsoftware.org/isinfo.php)

[link-1]: https://web.archive.org/web/20100918184438/http://permalink.gmane.org:80/gmane.comp.python.py2exe/3889
[link-2]: https://web.archive.org/web/20070209112832/http://www.mapr.ucl.ac.be:80/%7Egustin/win32_ports/pygtk.html

[link-3]: https://web.archive.org/web/20100816021243/http://library.gnome.org:80/devel/pygtk/stable/class-gtkbuilder.html
[link-4]: https://sourceforge.net/projects/gladewin32/files/gtk%2B-win32-runtime/2.8.14/
[link-5]: https://web.archive.org/web/20070209112832/http://www.mapr.ucl.ac.be:80/%7Egustin/win32_ports/pygtk.html
