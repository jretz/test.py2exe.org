= Environment =
The py2exe distribution contains a sample named ''hello.py'' together with a setup script to build an executable.  The script can be used to explore the differences in the runtime environments between the Python script, run with the Python interpreter, and the executable.

== special attributes of the sys module ==
 * {{{sys.path}}} contains only a single entry: the full pathname of the shared code archive.

 * {{{sys.prefix}}} contains the directory name of the shared code archive.

 * {{{sys.executable}}} is set to the full pathname of the exe-file.

 * The first item in {{{sys.argv}}} is the full pathname of the executable, the rest are the command line arguments.

 * {{{sys.frozen}}} only exists in the executable.  It is set to {{{"console_exe"}}} for a console executable, to {{{"windows_exe"}}} for a console-less gui executable, and to {{{"dll"}}} for a inprocess dll server.

 * {{{sys.frozendllhandle}}} only exists in inproc dll servers, it is set to the numerical value of the win32 dll handle.

== misc ==
 * {{{__file__}}} is not defined (you might want to use sys.argv[0] instead)
