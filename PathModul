= Problem =

Using the [[http://www.jorendorff.com/articles/python/path/|PathModule]] from  Jason Jorendorff, modulefinder.py, which is called by Py2Exe, gets into an endless recursion. 

It tries to resolve {{{os.path}}}, gets to {{{ os.os.path }}}, further to {{{ os.os.path }}} and breaks somewhere at 
{{{os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.os.path }}} at which point you get a {{{RuntimeError: maximum recursion depth exceeded}}}.

(Maybe it would be a test to use [[http://www.stackless.com/|StackLess]] Python, it would run forever or until the maximum string length of pyhton is reached. But maximum string length in Python is only limited by memory, memory is limited by address-space ... )

But apart from joking: it is IMPOSSIBLE to generate an exe with the modern 0.5 Version of Py2Exe when path.py is installed. 

= Workaround =
Just rename
{{{
site-packages/path.py
}}}

to 
{{{
site-packages/jpath.py
}}}

and make sure also to toggle your imports to
{{{
#!python
import jpath
}}}

and to delete {{{path.pyc}}} and {{{path.pyo}}} from your {{{site-packages}}} directory.

20041013HAM

= Possible Bugfix =

This patch to {{{Lib/modulefinder.py}}} ''should'' fix the problem, it would be nice if people would '''try it out, and report back''' here:
{{{
#!python
Index: modulefinder.py
===================================================================
RCS file: /cvsroot/python/python/dist/src/Lib/modulefinder.py,v
retrieving revision 1.7.6.1
diff -c -r1.7.6.1 modulefinder.py
*** modulefinder.py	14 Nov 2003 10:23:03 -0000	1.7.6.1
--- modulefinder.py	30 Mar 2004 18:54:01 -0000
***************
*** 245,250 ****
--- 245,253 ----
          if self.badmodules.has_key(fqname):
              self.msgout(3, "import_module -> None")
              return None
+         if parent and parent.__path__ is None:
+             self.msgout(3, "import_module -> None")
+             return None
          try:
              fp, pathname, stuff = self.find_module(partname,
                                                     parent and parent.__path__, parent)

}}}


Works for me on a simple test -- Paul Moore
<<BR>>Works for me -- Maxime Vernier
<<BR>>Works for me too -- Matteo Bertini
