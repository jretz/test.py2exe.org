= Where to correct =

Within site-packages/py2exe/samples/extending/setup.py

(line 54 ff..)
{{{
#!python
################################################################
# arguments for the setup() call

test_wx = dict(
    script = "test_wx.py",
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="test_wx"))],
    dest_base = r"prog\test_wx")

zipfile = r"lib\shardlib"

options = {"py2exe": {"compressed": 1,
                      "optimize": 2}}

################################################################
}}}
= what to do =

The Error is within 

{{{
#!python
zipfile = r"lib\shardlib"
}}}

it has to be

{{{
#!python
zipfile = r"lib\shardlib.zip"
}}}


= additional information =

I stumbled upon while trying to include win32com.client  - that module was not able to find {{{gen_py/__init__.py}}}

20040112 HAM



= the cause =

This problem is a limitation of the current win32all (build 163, currently).

Py2Exe itself does not require that the zipfile has a {{{.zip}}} extension (and this can be useful to obscure the contents of this file).

I've sent Mark Hammond a patch ;-)

-- Thomas Heller
