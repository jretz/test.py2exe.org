== How to exclude DLLs from the distribution ==

Sometimes, Python extensions require supporting DLLs from the system. One example of this is cx_Oracle, which requires the Oracle client software in order to do its job. Because cx_Oracle.pyd depends on the Oracle OCI library, py2exe's dependency tracking includes the file OCI.dll from the Oracle distribution in the distribution directory.

However, it is '''not''' appropriate to include OCI.dll with your software, as it is specific to the version of the Oracle client software on the target machine, and is not useful in isolation.

So, you need to tell py2exe to exclude this DLL from the resulting distribution. The dll_excludes option lets you do this (it's documented in the docstring for the py2exe module). It does not work from the command line, but you can include it in your setup.py as described in PassingOptionsToPy2Exe

{{{
    setup(
        options = {"py2exe": { "dll_excludes": ["oci.dll"]}},
        ...
    )
}}}
