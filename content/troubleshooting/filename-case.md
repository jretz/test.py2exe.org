= Filename Case Matters =

If your program works OK on one drive or filing system 
but not on another, or builds correctly on one filing 
system but not another, the problem may be due to 
case-mangling of filenames.

== Symptoms ==
Otherwise inexplicable errors about modules 
not being found. These will be modules whose names
are mixed-case (e.g. UserDict).
This can affect .dll names too.

== Likely causes ==
Netware or other filesystems that 
force "8.3" filenames to upper case, or Samba 
filesystems with either "preserve case = No" or "short preserve case = No" in smb.conf.

== Solutions ==

 * Build and execute only on a local hard drive.
 * Set up Samba with "preserve case = Yes" and "short preserve case = Yes".
 * Netware seems to preserve case of filenames contained in a folder if the folder itself has a long name.

