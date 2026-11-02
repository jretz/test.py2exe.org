# Distribution size

## Size does matter

In some cases (e.g. internet distribution) you'll want your distribution to be
as small as possible, and here are some tips for achieving this.

**Note**: the following methods all require passing options to py2exe. Check out
[Passing options](../build/passing-options.md) and
[Options](../build/options.md) for more information about passing options.
Also, at the end of the page is a code example including everything discussed
here.

## Compression

For the price of running a tad slower, you can compress the library zip using
the *compress* option.

## Encodings

py2exe automatically includes the entire encodings library in the distribution.
If you're **absolutely sure** you won't need to deal with Unicode (or any kind
of encoding) you can specify *ascii=True*, saving a lot of space by excluding
the encodings.

## Exclude \_ssl

Since the socket module imports the \_ssl module, every program using sockets
will include the \_ssl.pyd dll, which is pretty big. If you're using sockets but
don't need ssl, specify *excludes=\['\_ssl'\]*.

## Exclude standard libraries

py2exe also includes many unnecessary standard modules and libraries. There are
2 steps you can take in order to save this space:

### Exclude big modules

The following modules take a lot of space and are seldom used in distributions:

- doctest
- pdb
- unittest
- difflib
- inspect

If you're not using some or all of them, you can add them to the *excludes*
list.

### Do it yourself

Of course, another (and probably better) way to do this is simply open the
library.zip file py2exe created and look for big modules/packages, then add them
to the *excludes* list.
For example, I had the pyreadline package installed, and it ended up being
included in full, even though the program doesn't use it at all.

## Exclude msvcr71.dll

In Python versions before 2.6, py2exe puts the MS Visual C runtime DLL in your
distribution folder. Since most Windows installations nowadays include this DLL
by default, it may be unnecessary.
So again, only if you're **absolutely sure** everyone using the program will
already have msvcr71.dll, specify *dll\_excludes=\['msvcr71.dll'\]*.

## Example

Here is an example - my setup script, which resulted in a total size of 2.15 MB,
2.01 of which are the Python DLL (which of course can't be excluded).

```python
from distutils.core import setup
import py2exe

import sys; sys.argv.append('py2exe')

py2exe_options = dict(
                      ascii=True,  # Exclude encodings
                      excludes=['_ssl',  # Exclude _ssl
                                'pyreadline', 'difflib', 'doctest', 'locale', 
                                'optparse', 'pickle', 'calendar'],  # Exclude standard library
                      dll_excludes=['msvcr71.dll'],  # Exclude msvcr71
                      compressed=True,  # Compress library.zip
                      )

setup(name='<Name>',
      version='1.0',
      description='<Description>',
      author='Ofer Schwarz',

      console=['script.py'],
      options={'py2exe': py2exe_options},
      )
```
