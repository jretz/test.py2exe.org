# Logging

## logging module and %(filename)s

When using the logging module, the %(filename)s format option doesn't work. It
always ends up in the output as "\_ \_init\_ \_.pyo".

The problem is that the module uses source file names to determine when it has
walked back on the stack to the caller. In the py2exe environment, this
(fragile) logic breaks. The following code will workaround the problem.

### Example

```python2
import sys
if hasattr(sys, "frozen"):
    import logging
    logging._srcfile = r"logging\__init__.pyo"
```

Note, this is in a Windows environment. The '\\' should probably be replaced
with a '/' for a Unix environment.

Update: this issue was opened as ticket 1276210 with the Python folks at
SourceForge and they've checked in a fix as of 2005/09/02. No idea what release
that will be available in.
