# Subprocess

## Inheriting handles in child process

In subprocess.Popen, if you pass None for any of stdin, stdout
or stderr args (the default), then the subprocess is supposed
to inherit the corresponding parent process handle. However,
if you used py2exe to create a Windows program as opposed to a
console program, and you launched the py2exe program by
clicking rather than by running if from a command window, then
the parent process has no handle to inherit. subprocess.Popen
will throw an exception. In some instances it will throw
"TypeError: an integer is required" because GetStdHandle
returns None. In other cases it will throw "WindowsError:
\[Errno 6\] The handle is invalid" as shown in the traceback
below:

```python2
     File "subprocess.pyc", line 533, in __init__
     File "subprocess.pyc", line 607, in _get_handles
     File "subprocess.pyc", line 634, in _make_inheritable
   WindowsError: [Errno 6] The handle is invalid
```

This bug appears to be present up through at least Python 2.5.1
and can be found at
[http://sourceforge.net/tracker/index.php?func=detail&amp;aid=1124861&amp;group\_id=5470&amp;atid=105470][link-1]

The solution is not to pass None but rather specify a handle
for any of stdin, stdout and stderr that you don't want to
pipe.

Note also that when you create a windows program with py2exe,
sys.stderr is not a normal file object, so you can't use that,
but you can use sys.stderr.\_file buried inside it.

### Example

```python2
if hasattr(sys.stderr, 'fileno'):
    childstderr = sys.stderr
elif hasattr(sys.stderr, '_file') and hasattr(sys.stderr._file, 'fileno'):
    childstderr = sys.stderr._file
else:
    # Give up and point child stderr at nul
    childStderrPath = 'nul'
    childstderr = file(childStderrPath, 'a')
                
child = subprocess.Popen(...other args...
                         stderr = childstderr)

```

## Controlling appearance of child process created with py2exe

Suppose you want to launch a child process that is a py2exe program. If you want
to communicate with the child process via pipes attached to stdin or stdout,
then you must make it a console process. If you make it a windows process, then
sys.stdout is replaced with a Blackhole object that throws an exception when
written to. However, if you make it a console process, then, if it launched from
a non-console process a console window appears - ugly. The solution is to make
the child process a console process, but tell subprocess to launch it without a
console window.

### Example

```python2
child = subprocess.Popen(...other args...
                         creationflags = win32process.CREATE_NO_WINDOW)

```

-- [Alec Wysoker](mailto:alecw@pobox.com)

[link-1]: http://sourceforge.net/tracker/index.php?func=detail&aid=1124861&group_id=5470&atid=105470
