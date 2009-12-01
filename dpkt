dpkt, available at http://code.google.com/p/dpkt/ does not compile with py2exe.

After compiling and running a program that uses dpkt you will see an error like
{{{
Traceback (most recent call last):
  File "main.py", line 1, in <module>
  File "pcapcompare\__init__.pyc", line 2, in <module>
  File "pcapcompare\DataSection.pyc", line 1, in <module>
  File "dpkt\__init__.pyc", line 45, in <module>
  File "dpkt\ppp.pyc", line 63, in <module>
  File "dpkt\ppp.pyc", line 52, in __load_protos
WindowsError: [Error 3] The system cannot find the path specified: 'C:\\PcapCompare\\src\\dist\\library.zip\\dpkt
/*.*'
}}}

Several classes in dpkt use a function called {{{__load_protos()}}} to initialize some of their class attributes.  This function does not work with py2exe for the same [[ConfigImportProblems|reason that Biopython does not work with py2exe]].  The line to be changed reads:
{{{#!python
d = dict.fromkeys([ x[:-3] for x in os.listdir(os.path.dirname(__file__) or '.') if x.endswith('.py') ])
}}}
Replace that line with this:
{{{#!python
if hasattr(dpkt, '__loader__'):
    zipfiles = dpkt.__loader__._files
    x = [zipfiles[file][0] for file in zipfiles.keys() if 'dpkt\\' in file]
    d = dict.fromkeys([ y[:-4] for y in x if y.endswith('.pyc') ])
else:
    d = dict.fromkeys([ x[:-3] for x in os.listdir(os.path.dirname(__file__) or '.') if x.endswith('.py') ])
}}}

These files need the fix:
 * ethernet.py:102
 * ip.py:245
 * ppp.py:52

I fixed those files and was able to compile and run my program that uses dpkt.  Hopefully this fix is the correct fix.  I didn't take the time to understand why the fix was necessary, all I did was copy what the Biopython guy did.
