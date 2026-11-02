# Passing options

## Avoid sys.argv to pass options to py2exe

Many users write a special setup script for py2exe that simply can be run to
build the exe, without the need to specify command line options by hand, each
time. That means that "includes", "excludes" options etc have to be passed in
some way to py2exe.

The `setup()` function accepts a `options` keyword argument, containing a
dictionary with the options. This is superior to appending options to `sys.argv`
as the transformation of the data to a string and back is avoided as well as
mutiple `setup()` calls per file are possible.

Note that the long name of options has to be used and '-' in the command line
options become '\_' in the dictionary (e.g. "dist-dir" becomes "dist\_dir").

```python2
opts = {
    "py2exe": {
        "includes": "mod1, mod2",
        "dist_dir": "bin",
    }
}
```

And pass it to the setup script:

```python2
setup(
    options = opts,
    ...
)
```

## Avoid using setup parameters that are py2exe-specific

Instead of passing options like `console`, `windows` to `setup()`, you can
subclass Distribution and initialize them as follows:

```python2
from distutils.core import Distribution
class MyDistribution(Distribution):
    def __init__(self, attrs):
        self.com_server = []
        self.services = []
        self.windows = []
        self.console = ['myapp']
        self.zipfile = 'mylibrary.zip'
        Distribution.__init__(self, attrs)

setup(distclass=MyDistribution)
```
