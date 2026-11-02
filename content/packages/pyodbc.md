# PyODBC

If a script frozen with py2exe utilizes
[pyodbc](http://code.google.com/p/pyodbc/), running the executable version
produces the error:
`RuntimeError: Unable to import decimal`

The solution is to include the following py2exe option:

```python2
setup(
    ...
    options = {
        'py2exe': {
            'includes': 'decimal',
            },
        },
    ...
    )
```

Original solution was found in
["Compiled Python App Problem" thread on Dev Shed™ Forums][link-1].

[link-1]: http://forums.devshed.com/python-programming-11/compiled-python-app-problem-502516.html
