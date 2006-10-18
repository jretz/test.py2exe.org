py2exe does not currently (as of 0.6.5) work out of the box if some of your program's dependencies are in .egg form.

== Unzipping the .eggs ==
If your program does not itself use setuptools facilities (eg, pkg_resources), then all you need to do is make sure the dependencies are installed on your system in unzipped form, rather than in a zipped .egg.

One way to achieve this is to use the {{{--always-unzip}}} option to easy_install.

Another is to avoid easy_install by using {{{python setup.py install_lib}}} (and also {{{install_data}}} and {{{install_scripts}}}, if necessary) when installing the dependencies.

The result is a normal {{{Library.zip}}} which includes the dependency's files along with all the others.

== Namespaced Packages ==
If you have namespaced packages installed using the instruction above, you might need to do some extra work. In addition to:

{{{
__import__('pkg_resources').declare_namespace(__name__)}}}
... you will need to add:

{{{
import modulefinder
for p in __path__:
   modulefinder.AddPackagePath(__name__, p)}}}
That will make sure all the namespaced package directories are added to the internal registry in modulefinder, which is re-used by py2exe when looking for modules.

== Including .egg files in your dist directory ==
Alternatively, you can include the .egg in your dist directory by the following method.

This is an ugly hack that, I assume, will go away some day when py2exe is aware of eggs. The good thing about this hack is that the basic principles work with both py2exe and py2app.

This is cut from a couple spots in my script. The basic flow is:

 1. unpack zipped eggs, because I believe py2exe chokes on them when resolving dependencies
 1. keep track of the top level packages in the eggs
 1. add all of the files in the eggs to the data_files, so that the eggs are installed along side the main exe
 1. build the exe
 1. generate a new library.zip that does not include anything in the top level packages found in step 2
here's steps 1 and 2:

{{{
import pkg_resources
eggs = pkg_resources.require("TurboGears")
from setuptools.archive_util import unpack_archive
for egg in eggs:
   if os.path.isdir(egg.location):
       sys.path.insert(0, egg.location)
       continue
   unpack_archive(egg.location, eggdir)
eggpacks = set()
eggspth = open("build/eggs.pth", "w")
for egg in eggs:
   print egg
   eggspth.write(os.path.basename(egg.location))
   eggspth.write("\n")
   eggpacks.update(egg.get_metadata_lines("top_level.txt"))
eggspth.close()
eggpacks.remove("pkg_resources")
}}}
and here's step 5:

{{{
   import zipfile
   oldzipfile = "dist/exe/library.zip"
   newzipfile = "dist/exe/small-library.zip"
   oldzip = zipfile.ZipFile(oldzipfile, "r")
   newzip = zipfile.ZipFile(newzipfile, "w", zipfile.ZIP_STORED)
   for entry in oldzip.infolist():
       delim = entry.filename.find("/")
       if delim == -1:
           delim = entry.filename.find(".")
       if delim > -1:
           if entry.filename[0:delim] in eggpacks:
               print "Skipping %s, it's in the egg" % (entry.filename)
               continue
       newzip.writestr(entry, oldzip.read(entry.filename))
   newzip.close()
   oldzip.close()
   os.remove(oldzipfile)
   os.rename(newzipfile, oldzipfile)
}}}
