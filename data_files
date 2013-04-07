The data_files allows you to include one (or more) series of files that you are going to need to run your executable.   For example, to run a GUI executable, I use data_files to create a folder in my dist directory called "images" and copy my list of image files over.

The data_files takes a tuple 1) the location to store the data and 2) the location to copy the data from

Example:

{{{#!python
from distutils.core import setup
import py2exe

Mydata_files = [('images', ['c:/path/to/image/image.png'])]

setup(
    console=['trypyglet.py.py'],
    data_files = Mydata_files,
    options={
                "py2exe":{
                        "unbuffered": True,
                        "optimize": 2,
                        "excludes": ["email"]
                }
        }
)
}}}
More often you'll have a directory of image files, and you can use some code to push the directory into a list:

Example:

{{{#!python
import os
from distutils.core import setup
import py2exe

Mydata_files = []
for files in os.listdir('C:/path/to/image/directory/'):
    f1 = 'C:/path/to/image/directory/' + files
    if os.path.isfile(f1): # skip directories
        f2 = 'images', [f1]
        Mydata_files.append(f2)

setup(
    console=['trypyglet.py.py'],
    data_files = Mydata_files,
    options={
                "py2exe":{
                        "unbuffered": True,
                        "optimize": 2,
                        "excludes": ["email"]
                }
        }
)
}}}
A helpful function:

{{{#!python
import os
import glob

def find_data_files(source,target,patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
    return sorted(ret.items())

# Example:
setup(
    name="Sample",
    version="1.0",
    description="A sample app",
    author="MizardX",
    console=['samplescript.py'],
    data_files=find_data_files('data','',[
        'README',
        'images/*',
    ]),
)

# Will copy data/README to dist/README, and all files in data/images/ to dist/images/
# (not checking any subdirectories of data/images/)
}}}
