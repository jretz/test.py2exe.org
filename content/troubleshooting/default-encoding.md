# even more encoding

## Description

Some (at least me :) are working with a different default-encoding than "ASCII".
I am using Latin-1, which solves 98% of encoding problems when dealing with
Windows-Applications on a German Windows.

so in site.py I changed from ASCII to LATIN-1

## Problem

When an application is py2exed, site.py is not available and not parsed. (and
that is good)

So the behaviour of the py2exed and the python filename.py use of the
application is quite different.

## Solution

Top of the application I start with

```python
import sys
# sys.setdefaultencoding may be deleted by site.py, 
# so bring it back:
reload(sys) 
if hasattr(sys,"setdefaultencoding"):
    sys.setdefaultencoding("latin-1")

```

### Another solution

To take a guess at the users preferred encoding, do like the disabled code in
site.py does:

```python
import sys
if hasattr(sys, 'setdefaultencoding'):
    import locale
    loc = locale.getdefaultlocale()
    if loc[1]:
        encoding = loc[1]
        sys.setdefaultencoding(encoding)

```

## Explanation

if site.py is run, it kills the "setdefaultencoding" attribute.

HAM20040806 - we need a ternary decorator
