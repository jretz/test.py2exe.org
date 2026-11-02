# PackageLoader issues

If you get a message like `ImportError: cannot import name factorial` (see
<http://article.gmane.org/gmane.comp.python.py2exe/3324> or
<http://mail.scipy.org/pipermail/scipy-user/2009-May/021216.html>), this is due
to a failure in a somewhat-magical mechanism that Scipy uses to import symbols
into the top-level scipy module. Rather than, e.g., `from scipy.x.y import *`,
it uses a Numpy mechanism called `PackageLoader`, which uses info.py files in
each submodule to know what symbols to import. Those files do seem to be making
it into the py2exe distribution, but they're not getting used correctly. I'm not
sure if the bug is scipy or py2exe.

A hackish workaround is to modify `scipy/__init__.py` to explicitly import the
symbols you need, e.g., `from scipy.misc import factorial`.

## Brian K. Boonstra

### The problem

When using py2exe with scipy, you end with messages about missing modules. Some
of them may not end up mattering (as in my case where scipy\_base.add was
missing) but others do, notably `__cvs_version__` modules of some scipy
packages, plus the `cephes` module.

### The solution

You just need a few includes. Here is what I have:

```python2
excludes = []
includes = ["scipy.special.__cvs_version__", "scipy.linalg.__cvs_version__", "scipy.special.cephes"]

opts = {
    "py2exe": {
        "includes":includes,
        "excludes":excludes
    }
}

setup(...
     com_server=['myserver'],
     options=opts
        )

```

but if your code actually uses more of the scipy packages, you might need to add
a few more `__cvs_version__` entries.

---

CategoryHomepage
