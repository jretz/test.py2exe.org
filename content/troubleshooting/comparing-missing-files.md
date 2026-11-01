For what ever reason py2exe wasn't automatically importing in some miscellaneous stuff. As the project was very large it was hard to tell quickly what might be missing. Folder comparison tools didn't really help since there was just enough difference between the files to make them catch just about everything. So I broke down and pieced this together. Since I'm new to Python I'm sure there are better ways to do this but this does work. Feel free to hack away at it. -- Aaron R. Short

{{{
# Author: Aaron R. Short
# Date: April 10, 2009
# File: comparison.py
# This is a quick hack to find which files, packages, and or modules didn't
# make it over in py2exe setup. To use unzip your libary.zip so that the
# directories should be similar. Also if you don't clear your build directory
# every run you might want to delete that as well.

import os
import glob
import string

sourcepath = 'the source code path'
distpath = 'the destination path'

sourcelist = []
    
for root, dirs, files in os.walk(sourcepath):
    for name in files:
        pathfile = os.path.join(root, name)
        
        #ignore python extensions
        pathfile = string.replace(pathfile, '.pyo', '') 
        pathfile = string.replace(pathfile, '.pyc', '')
        pathfile = string.replace(pathfile, '.py', '')
        #remove root path
        pathfile = string.replace(pathfile, sourcepath, '') 
        sourcelist.append(pathfile)

distlist = []
    
for root, dirs, files in os.walk(distpath):
    for name in files:
        pathfile = os.path.join(root, name)
        
        #ignore python extensions
        pathfile = string.replace(pathfile, '.pyo', '') 
        pathfile = string.replace(pathfile, '.pyc', '')
        pathfile = string.replace(pathfile, '.py', '')
        
        #remove root path      
        pathfile = string.replace(pathfile, distpath, '')   
        distlist.append(pathfile)

sourceset = set(sourcelist)
distset = set(distlist)

missing = sourceset - distset        

for (files) in sorted(missing):
    print files
}}}
