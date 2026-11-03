# os.popen

## os.popen

os.popen() doesn't work when the CWD is a UNC path like
`\\hostname\dirname\...`.

The call to os.popen() will
appear to succeed, but subsequent calls to read/write the
returned pipe will result in an `IOError: invalid parameter`
exception.

This failure is not specific to py2exe as it will happen
anytime os.popen() is used with a current working directory
(CWD) that is a UNC path such as `\\hostname\dirname\...`
rather than a DOS style path such as `G:dirname`. While
this isn't specific to py2exe, the problem is rarely
encountered unless a program has been distributed using
something like py2exe and is being executed by clicking on a
file or shortcut to which the user has browsed on the network.

The underlying problem is due to a "feature" in cmd.exe
documented at <https://jeffpar.github.io/kbarchive/kb/156/Q156276/>

The solution is to use subprocess.Popen() with shell=False
(which won't use cmd.exe) instead of os.popen() (which does use
cmd.exe). However, subprocess.Popen() has its own
Windows-related bug which requires working around. See the
subprocess documentation at
<https://docs.python.org/2.7/library/subprocess.html> for
general usage and [Subprocess](subprocess.md) page for
examples on working around subprocess.Popen bugs that show up
when using py2exe.
