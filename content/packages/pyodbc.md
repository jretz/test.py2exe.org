= PyODBC =

If a script frozen with py2exe utilizes [[http://code.google.com/p/pyodbc/|pyodbc]], running the executable version produces the error:
{{{RuntimeError: Unable to import decimal}}}

The solution is to include the following py2exe option:

{{{
setup(
    ...
    options = {
        'py2exe': {
            'includes': 'decimal',
            },
        },
    ...
    )
}}}

Original solution was found in [[http://forums.devshed.com/python-programming-11/compiled-python-app-problem-502516.html|"Compiled Python App Problem" thread on Dev Shed™ Forums]].
