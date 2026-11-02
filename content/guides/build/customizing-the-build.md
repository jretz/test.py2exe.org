# customizing py2exe by subclassing

Let's say you're not entirely happy with one detail in the build process of
py2exe. That may be because you want to filter the list of files that it
collects or something else.

Make subclass of py2exe and override the methods you want to change:

```python2
from py2exe.build_exe import py2exe as build_exe
class my_py2exe(build_exe):
    ....
```

Then in the setup() call we need to tell
[Distutils](../../getting-started/distutils.md) that it should use our class:

```python2
setup(...
      cmdclass = {"py2exe": my_py2exe},
      ...
)
```

In fact, that mechanism allows to install any
[Distutils](../../getting-started/distutils.md) command.
