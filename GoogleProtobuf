= google.protobuf =

http://code.google.com/p/protobuf/ is packaged as `google.protobuf`, but contains no `google/__init__.py` file, so `google` doesn't seem a valid package to py2exe, and it says ''The following modules appear to be missing'' for `google` and `google.protobuf`

Workaround is to create an empty `__init__.py` file in the `google` directory before running py2exe
