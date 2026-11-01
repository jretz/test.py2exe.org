Pythoncard has 2 problems. 


 1. the resources (gui screens) dont get copied
 2. the components dont get copied

Heres a fix that only touches your setup.py file. Its not perfect
but it is not bad for starters.

{{{
from distutils.core import setup

# py2exe stuff
import py2exe, os
# find pythoncard resources, to add as 'data_files'
pycard_resources=[]
for filename in os.listdir('.'):
    if filename.find('.rsrc.')>-1:
        pycard_resources+=[filename]

# includes for py2exe
includes=[]
for comp in ['button','image','staticbox',\
            'statictext','textarea','textfield','passwordfield']:
    includes += ['PythonCard.components.'+comp]
print 'includes',includes

opts = { 'py2exe': { 'includes':includes } }
print 'opts',opts
# end of py2exe stuff

setup(name='blarg',
    version='0.1',
    url='about:none',
    author='anonymous',
    author_email='root@127.0.0.1',
    package_dir={'blarg':'.'},
    packages=['blarg'],
    data_files=[('.',pycard_resources)],
    console=['blarg.py'],
    options=opts
    )



}}}
