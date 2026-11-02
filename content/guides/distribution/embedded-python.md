# Embedded Python

## How can py2exe help shipping emedded Python projects

An embedded Python project relies on several modules. Finding these modules is
very easy using py2exe.

Create a *setup.py* script with the following lines:

```python2
 
from distutils.core import setup
import py2exe

setup()
```

And then run it with your script in the command line

```doscon
python setup.py py2exe --includes mymodule
```

This will create a *dist* directory with all the files your embedded python
needs.
Rename *library.zip* to *python23.zip* and place all the files in the
application directory.

Miki &lt;<miki.tebeka@zoran.com>&gt;
