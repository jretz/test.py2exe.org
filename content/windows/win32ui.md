# win32ui

## The Problem

A python program containing :

```python
import win32ui
```

generates an error in .exe mode (i.e. after being compiled with py2exe) :

```py2tb
Traceback (most recent call last):
  File "test_win32ui.py", line 5, in <module>
    import win32ui
  File "win32ui.pyo", line 12, in <module>
  File "win32ui.pyo", line 10, in __load
ImportError: DLL load failed: This application has failed to start because the application configuration is incorrect. Reinstalling the application may fix this problem.
```

## Explanation

win32ui needs the MFC (Microsoft Foundation Classes) DLLs to run in .exe mode.

## Solution

### Ship the needed DLLs with the application

The DLLs and a manifest file can be found in :
"C:\\Python26\\Lib\\site-packages\\pythonwin\\"

You will need the following files :

- mfc90.dll
- mfc90u.dll
- mfcm90.dll
- mfcm90u.dll
- Microsoft.VC90.MFC.manifest

To copy files at compile time, add or modify the data\_files option in your
setup.py :

```python
mfcfiles = [os.path.join(mfcdir, i) for i in ["mfc90.dll", "mfc90u.dll", "mfcm90.dll", "mfcm90u.dll", "Microsoft.VC90.MFC.manifest"]]

data_files = [("Microsoft.VC90.MFC", mfcfiles),
              ]

setup(
    data_files = data_files,
    ...
  )
```

With this in place, running py2exe should put the files into your dist
directory:

```output
  dist
  |
  +-Microsoft.VC90.MFC
  | |
  | +-Microsoft.VC90.MFC.manifest
  | +-mfc90.dll
  | +-...
  |-...
```

### Install "vcredist"

An alternative solution is to install the "Microsoft Visual C++ 2008
Redistributable Package". See [Tutorial](../getting-started/tutorial.md#Step522)
