# GUI console output

A GTK application I made has unimported errors. I used the option 'windows', but
the console window gets opened when getting an error.
And maybe a tip, when closing the program it should be optional whether or not
it warns for errors.

Mark Baas &lt;m.baas \_at\_ zarb.org&gt;

You can always redirect where the errors go with the sys module.
sys.stderr = StringIO.StringIO() will redirect error messages to a string in
your program that no one will ever see.

A better option is a log file, then they can see the errors if the want to but
don't have to
sys.stderr = open("logfile.txt","w")

if you want to redirect print statements as well, point sys.stdout to some other
file

To avoid runtime errors on closing the windows executable, it may help to
suppress all output and
modify py2exe/boot\_common.py to

```python2
if sys.frozen == "windows_exe" :
    class Blackhole(object):
        softspace = 0
        def write(self, text):
            pass
    sys.stdout = Blackhole()
    sys.stderr = Blackhole()
    del Blackhole
del sys
```

\[Added by timo (at) eda-solutions.de\]

See [Error logging](error-logging.md) for more info on this subject.
