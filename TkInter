= Problem =
I use wxPython for my GUI. Modulefinder / py2exe nonetheless decides that tkinter and tcl have to be included in my distribution.
= Explanation =
??? I would like one, really. 
And I found one, with help of Thomas:
I included SimpleXMLServer, which itself has a conditional import of pydoc, which has a conditional import of tkinter.
But conditional or not, I do not want tkinter in my distribution. So I staid with my solution
ham 2004-02-01

I have tried removing the pydoc import in SimpleXMLServer, but py2exe keeps importing tcl. So it must be something else. -- Dody Wijaya

= Solution =
Extend the exclusions
{{{
#!python
excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list", 
            "Tkconstants","Tkinter","tcl"
            ]
}}}

the relevant line is
{{{
            "Tkconstants","Tkinter","tcl"
}}}
HAM 20040127

= Amendment if you're using PIL =

I'm using PIL in my application and it has a bunch of Tk files and dependencies in it which aren't explicitly necessary if you're not using Tk.

 <!> First, when you're trying to resolve issues where files aren't getting excluded or included properly, make sure to erase your {{{build}}} directory.  That saves a lot of headaches right there, where Python or py2exe or both are seeing old, non-excluded compiled versions of files.  Thanks to {{{ drewp }}} on {{{ #python }}} for the reminder.

Per {{{ The-Fixer }}} in {{{ #python }}}, changing my Python app extension from {{{ .py }}} to {{{ .pyw }}} got rid of many of the additional modules being included.  Eir's not sure why, and I'm not either, but it makes a difference to py2exe.  There are still a handful of files laying around, though.  Although they only add up to about 11K (and less when zipped), it's the principle of the thing.  :)

To really clean house, along with the three excludes listed above, add the following to your {{{ setup.py }}} to get rid of the remaining rogue elements.  

{{{
            "_imagingtk", "PIL._imagingtk", "ImageTk", "PIL.ImageTk", "FixTk"
}}}

Yes, you do have to double up on the definitions.  You can also now change your extension back to {{{ .py }}} if you want; that makes no difference after you exclude all of the above.

Thanks for the help!

-- Vito Miliano, 2005/04/16

