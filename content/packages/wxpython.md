# wxPython

**FIX**: Delete the *build* directory. Simple fix for an obscure and complicated
problem...

BTW: That Fix also helps with very very obscure DLL-Not-Found-Problems when
updating wxPython - HAM2004-08-30

I'm having some trouble using Python (2.3.4) with py2exe (0.5.0) and wxPython
(2.4.2.4). Without py2exe

> my program runs fine, and it compiles fine, but when I run the compiled
> executable it crashes with:

```py2tb
Traceback (most recent call last):
File "wxfoo.py", line 10, in ?
from wxPython.wx import *
File "wxPython\wx.pyc", line 4, in ?
File "wxPython\misc.pyc", line 15, in ?
File "wxPython\wx.pyc", line 6, in ?
File "wxPython\misc2.pyc", line 4, in ?
File "wxPython\windows.pyc", line 15, in ?
File "wxPython\wx.pyc", line 10, in ?
File "wxPython\gdi.pyc", line 15, in ?
File "wxPython\wx.pyc", line 12, in ?
File "wxPython\fonts.pyc", line 120, in ?
NameError: name 'wxObjectPtr' is not defined
```

All wxfoo.py contains is "from wxPython.wx import \*" and this happens with
every

> wxPython program I try. I've heard of people successfully py2exe'ing wxPython
> programs before so I wonder if doing something wrong. This is my setup.py:

```python
from distutils.core import setup
import py2exe
setup(console=["wxfoo.py"])
```

Anyone have any ideas whats wrong? options={"py2exe": {"includes":
"wxPython.wx}} and options={"py2exe": {"package": "wx"}} and windows=wxfoo.py
return the same results.

> *-jc*
I'm having a similar problem in WinXP. Boa Constructor doesn't work with
wxPython2.5(it needs 2.4.2.4) but the version of AccessGrid I'm running requires
wxPython2.5. I fould that if I just copy the wx and wxPython directories for
wxPython2.5 somewhere for safe keeping, then copy in the wx and wxPython
directories for wxPython2.4.2.4 Boa will run once. Then on successive attempts,
I get the "NameError: name 'wxObjectPtr' is not defined" message from fonts.py.
I did have a build directory in the wxPython directory and got rid of that, but
even now that the build directory is gone, I'm still getting the same problem.
Perhaps there's more to this story? -myk-

**FIX:** Add the missing DLL to the system folder.

When you package a wx application with py2exe, and the .exe file does not tun
successfully, simply copy the missing dll into your system folder. (In WinXP it
is often C:\\WINDOWS\\system32)

We hope that this bug will be fixed at the next py2exe release.

Note that if you are using the wxversion module in your program to select which
version of wx to use, you may need to make modifications to your code for
bundling the application with py2exe. See the wxversion documentation for more
details: <http://www.wxpython.org/docs/api/wxversion-module.html> ~JMH
