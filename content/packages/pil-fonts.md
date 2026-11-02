# PIL fonts

If you've been getting errors like this:

File "PIL\\ImageFont.pyc", line ---, in load\_path
IOError: cannot find font file

The fix is to simply copy the files helvetica-10.pil, helvB08.pil,
helvetica-10.png and helvB08.png into the "dist" directory.

It may also be needed to add current path in the load\_path() function in
ImageFont.py (otherwise it searches in sys.path directories only).
**for dir in sys.path+\['.'\]** instead of **for dir in sys.path**
