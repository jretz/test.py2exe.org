# General Tips and Tricks

- [Options](build/options.md) - How to see the list of available options for
  your setup.py script
- [Running setup](../getting-started/running-setup.md) - How to run the setup
  script once you've written it
- [Missing encodings](../troubleshooting/missing-encodings.md) - Problem with
  encodings and when they are not found in a standalone executable
- [Default encoding](../troubleshooting/default-encoding.md) - They really keep
  bugging. Solution to problem with different site.py
- [Configuration files](build/configuration-files.md) - How can you add
  arbitrary files to your py2exe-Setup?
- [Path module](../packages/path-module.md) - Using Jason Orendorffs python
  [Path module](../packages/path-module.md) together with py2exe 0.5
- [Passing options](build/passing-options.md) - Avoid using sys.argv to pass
  options
- [Customizing the build](build/customizing-the-build.md) - Customizing the
  build process
- [Icons](build/icons.md) - How to get your own icons with py2exe 0.5
- [Tkinter](../packages/tkinter.md) - I do not need any tkinter / tcl-Libs in my
  Setup
- [Filename case](../troubleshooting/filename-case.md) - Some windows filing
  systems mangle case, break py2exe programs
- [Batch builds](build/batch-builds.md) - A short Windows Batch File to fast
  provide the EXE File
- [Excluding DLLs](build/excluding-dlls.md) - Stopping py2exe from picking up
  unwanted DLLs
- [Embedded Python](distribution/embedded-python.md) - How to use py2exe to ship
  embedded Python modules
- [Single file executables](distribution/single-file-executables.md) - with NSIS
- [Optimized bytecode](optimization/optimized-bytecode.md) - How to get
  optimized bytecode for all modules
- [Embedded resources](build/embedded-resources.md) - Add custom data in the
  executable?
- [Detecting frozen programs](runtime/detecting-frozen-programs.md) - Simple
  functions to determine if you're in an .exe or .py
- [Locating the executable](runtime/locating-the-executable.md) - sometimes you
  need to now where your exe is within the filesystem
- [Environment](runtime/environment.md) - Information about the environment for
  the executable
- [Windows services](../windows/services.md) - some gained knowledge
- [GUI console output](runtime/gui-console-output.md) - dealing with stdout
- [Error logging](runtime/error-logging.md) - How does py2exe handle stack track
  printing and STDERR? How can Ichange that behaviour?
- [SOAPpy](../packages/soappy.md) - How to get SOAPpy working with py2exe.
- [PyBuilder](https://sourceforge.net/projects/pybuilder/) - A Gui interface to
  compile easier and
  faster.
- [DLL inclusion rules](build/dll-inclusion-rules.md) - how to override the
  criteria that py2exe uses to determine whether a DLL should be included in the
  distributed package.
- [Warnings](../troubleshooting/warnings.md) - what to do to avoid warnings in
  windows (no console) mode getting into application errors.
- [Distribution size](optimization/distribution-size.md) - how to make your
  distribution as small as possible
- [Comparing missing files](../troubleshooting/comparing-missing-files.md) - a
  quick script for finding missing files, packages, and modules.
