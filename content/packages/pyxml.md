# PyXML

If you're getting
File "xml\\sax\\saxexts.pyc", line 77, in make\_parser

xml.sax.\_exceptions.SAXReaderNotAvailable: No parsers found

Try adding this to your setup.py py2exe command line:
--packages xml.sax.drivers,xml.sax.drivers2
