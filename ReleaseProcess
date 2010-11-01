= Release Process =

This page is for the developers/maintainers. It contains the steps involved in making a new public release of py2exe.

   1. Change the {{{__version__}}} string in {{{py2exe\__init__.py}}}
   2. Update {{{ANNOUNCE}}} (be sure to change the version number on the first line)
   3. Update copyright date in {{{docs\license.txt}}} and {{{setup.py}}}
   4. Update {{{docs\py2exe.txt}}}
   5. Run {{{docs\html.cmd}}} to generate html
   6. Commit above files to svn
   7. Run {{{build.cmd}}} to build for all versions of Python
   8. Install for all versions of Python ({{{test\reinstall.cmd}}} can help)
   9. Run {{{test\test.py}}} to ensure everything works
   10. Tag all files in svn as release_x_y_z where x_y_z is {{{py2exe.___version___}}}
   11. [[https://sourceforge.net/project/admin/newrelease.php?package_id=35995&group_id=15583|Create a File Release on SourceForge]] (use {{{py2exe.___version___}}} as the release name)
   12. Run {{{docs\updateweb.cmd}}} to publish website
   13. Run {{{setup.py register}}} to update the Python Package Index
   14. Update [[News]]
   15. Send {{{ANNOUNCE}}} to py2exe-users, comp.lang.python, comp.lang.python.announce
   16. Change the {{{__version__}}} string in {{{py2exe\__init__.py}}} to a development version to distinguish it from released versions
   17. Commit above file to svn
