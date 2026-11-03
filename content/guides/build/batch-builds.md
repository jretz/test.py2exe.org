# Batch builds

## What is it

I use a short Windows Batch File to "automate" Py2EXE

How it works:

- Create the Py2EXE SetupFile
- Compile the Python Script
- Move the Py2EXE-Results to a Subdirectory
- Cleans the File-System (delete *build* and *dist*)
- Optional Recompress *library.zip* with [7-Zip](https://www.7-zip.org/)
- Optional Compress *\*.pyd*, *\*.dll* and *\*.exe* Files with
  [UPX](https://upx.github.io/)

(About Compression see [Compression](../optimization/compression.md) under *7ZIP
and UPX*)

## Instruction

I use it under Win XP... It should also run under NT and 2000, but i don't
know...

You must **change the Path** to the Apps in the Batch-File!!!

The BatchFile is very flexible, it uses its own file name to locate the Python
Script!  
You must **rename it** to exactly the same name like the script to compile.
Example:

- Name of the Pythonscript to Compile: MyScript.py
- You must rename the BatchFile to: MyScript.cmd

To change the content of the Py2EXE-Setup-File, you must change the
*:MakeSetupFile* section in the BatchFile

flexible?  
So you can quick use the Batch File with other Python script, yust copy and
rename it!

## The BatchFile

```bat
@echo off


::Set personal Path to the Apps:
set PythonEXE=C:\Python\python.exe
set SevenZipEXE=D:\Tools\7-ZIP\7z.exe
set UpxEXE=D:\Tools\upx\upx.exe


:: Compress=1 - Use CompressFiles
:: Compress=0 - Don't CompressFiles
set Compress=1


if not exist %~dpn0.py		call :FileNotFound %~dpn0.py
if not exist %PythonEXE%	call :FileNotFound %PythonEXE%
if not exist %SevenZipEXE%	call :FileNotFound %SevenZipEXE%
if not exist %UpxEXE%		call :FileNotFound %UpxEXE%


::Write the Py2EXE-Setup File
call :MakeSetupFile >"%~dpn0_EXESetup.py"


::Compile the Python-Script
%PythonEXE% "%~dpn0_EXESetup.py" py2exe
if not "%errorlevel%"=="0" (
	echo Py2EXE Error!
	pause
	goto:eof
)


:: Delete the Py2EXE-Setup File
del "%~dpn0_EXESetup.py"


:: Copy the Py2EXE Results to the SubDirectory and Clean Py2EXE-Results
rd build /s /q
xcopy dist\*.* "%~dpn0_EXE\" /d /y
:: I use xcopy dist\*.* "%~dpn0_EXE\" /s /d /y
:: This is necessary when you have subdirectories - like when you use Tkinter
rd dist /s /q


if "%Compress%"=="1" call:CompressFiles
echo.
echo.
echo Done: "%~dpn0_EXE\"
echo.
pause
goto:eof



:CompressFiles
	%SevenZipEXE% -aoa x "%~dpn0_EXE\library.zip" -o"%~dpn0_EXE\library\"
	del "%~dpn0_EXE\library.zip"

	cd %~dpn0_EXE\library\
	%SevenZipEXE% a -tzip -mx9 "..\library.zip" -r
	cd..
	rd "%~dpn0_EXE\library" /s /q

	cd %~dpn0_EXE\
	%UpxEXE% --best *.*
goto:eof



:MakeSetupFile
	echo.
	echo from distutils.core import setup
	echo import py2exe
	echo.
	echo setup (console=[r"%~dpn0.py"],
	echo    options = {"py2exe": {"packages": ["encodings"]}})
	echo.
goto:eof


:FileNotFound
	echo.
	echo Error, File not found:
	echo [%1]
	echo.
	echo Check Path in %~nx0???
	echo.
	pause
	exit
goto:eof
```
