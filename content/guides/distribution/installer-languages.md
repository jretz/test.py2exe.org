# Installer languages

Extending Thomas' "extending"-Example from
[py2exe](../../getting-started/overview.md) I customized my Setup-Routine. The
consumers of my software are German speaking, so I needed a German Setup
Assistent. So I added:

```python
    def create(self, pathname="dist\\dbeitrag.iss"):
        self.pathname = pathname
        ofi = self.file = open(pathname, "w")
        print >> ofi, "; WARNING: This script has been created by py2exe. Changes to this script"
        print >> ofi, "; will be overwritten the next time py2exe is run!"

        print >> ofi, """
[Languages]
Name: Deutsch; MessagesFile: "compiler:German-2-4.0.5.isl"
"""

        print >> ofi, r"[Setup]"
```

The Messagefile for German language I got from
[InnoSetup Translations](http://www.jrsoftware.org/files/istrans/).
It is even possible to provide a multitude of tranlations, say

```python
    def create(self, pathname="dist\\dbeitrag.iss"):
        self.pathname = pathname
        ofi = self.file = open(pathname, "w")
        print >> ofi, "; WARNING: This script has been created by py2exe. Changes to this script"
        print >> ofi, "; will be overwritten the next time py2exe is run!"

        print >> ofi, """
[Languages]
Name: Deutsch; MessagesFile: "compiler:German-2-4.0.5.isl"
Name: Italiano; MessagesFile: "compiler:Italian-12-4.0.8.isl"
Name: Ruski; MessagesFile: "compiler:Russian-17-4.0.3.isl"
Name: Norsk; MessagesFile: "compiler:NorwegianNynorsk-1-4.0.8.isl"
Name: Espagnol; MessagesFile: "compiler:Spanish-5-4.0.5.isl"
        """

        print >> ofi, r"[Setup]"
```
