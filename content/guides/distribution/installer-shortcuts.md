# Installer shortcuts

## Question

When presenting the first version of my Skript-Installer to the customer, the
reaction was "great, now we should automatically add links to Desktop and
Quickstart".
I was sure that it is possible.
And it was MUCH easier than suspected.

## Solution

```python
print >> ofi, r"[Files]"
        for path in self.windows_exe_files + self.lib_files:
            print >> ofi, r'Source: "%s"; DestDir: "{app}\%s"; Flags: ignoreversion' % (path, os.path.dirname(path))

        print >> ofi, """
[Tasks]
Name: "quicklaunchicon"; Description: "Icon in Schnellstartleiste erstellen"; GroupDescription: "Weitere Möglichkeiten, das Programm aufzurufen:"; Flags: checkedonce 
Name: "desktopicon"; Description: "Verknüpfung auf &Desktop erstellen"; GroupDescription: "Weitere Möglichkeiten, das Programm aufzurufen:"; Flags: checkedonce 
        """


        print >> ofi, r"[Icons]"
        for path in self.windows_exe_files:
            print >> ofi, r'Name: "{group}\%s"; Filename: "{app}\%s"' % \
                  (self.name, path)
        print >> ofi, 'Name: "{group}\Uninstall %s"; Filename: "{uninstallexe}"' % self.name
        print >> ofi, 'Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\%s"; Filename: "{app}\%s"; Tasks: quicklaunchicon' % (self.name, path)
        print >> ofi, 'Name: "{userdesktop}\%s"; Filename: "{app}\%s"; Tasks: desktopicon' % (self.name, path)

```

Essential are:

```ini
[Tasks]
Name: "quicklaunchicon"; Description: "Icon in Schnellstartleiste erstellen"; GroupDescription: "Weitere Möglichkeiten, das Programm aufzurufen:"; Flags: checkedonce 
Name: "desktopicon"; Description: "Verknüpfung auf &Desktop erstellen"; GroupDescription: "Weitere Möglichkeiten, das Programm aufzurufen:"; Flags: checkedonce 
```

With this tasks the text within Description is presented to the user. ("Create
Quicklink Icon", but in German). "checkedonce" presents this choice with the
first installation of the software checked, with subsequent installations
(without prio Deinstalltion) the Options are unchecked.

and

```python
        print >> ofi, 'Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\%s"; Filename: "{app}\%s"; Tasks: quicklaunchicon' % (self.name, path)
        print >> ofi, 'Name: "{userdesktop}\%s"; Filename: "{app}\%s"; Tasks: desktopicon' % (self.name, path)
```

is responsible for creating the appropriate Icons in Quickstart and on the
desktop. Statements "Tasks: desktopicon" gives only an Icon if the appropriate
option was checked during installation.

(that's more about [Innosetup](https://jrsoftware.org/isinfo.php) than
[py2exe](../../getting-started/overview.md), but ... both are free, both are
great and both are only one click away :)

20040113HAM
