# ZeroMQ

Recipe for py2exe and the zmq package

## Error message

```output
*** finding dlls needed ***
error: libzmq.dll: No such file or directory
```

or

```py2tb
Traceback (most recent call last):
  File "main.py", line 1, in <module>
  File "zmq\__init__.pyc", line 38, in <module>
  File "zmq\core\__init__.pyc", line 26, in <module>
  File "zmq\core\error.pyc", line 12, in <module>
  File "zmq\core\error.pyc", line 10, in __load
  File "error.pyx", line 34, in init zmq.core.error (zmq\core\error.c:1195)
ImportError: No module named strtypes
```

## Solution

```python
from py2exe.build_exe import py2exe
from distutils.core import setup
import os
import zmq

# libzmq.dll is in same directory as zmq's __init__.py

os.environ["PATH"] = \
    os.environ["PATH"] + \
    os.path.pathsep + os.path.split(zmq.__file__)[0]

setup( console=[{"script": "main.py"}],
       options={ 
           "py2exe": { 
               "includes": 
               ["zmq.utils", "zmq.utils.jsonapi", 
                "zmq.utils.strtypes"] } } )
```
