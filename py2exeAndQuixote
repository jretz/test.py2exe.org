= The Problem =

Quixote may use a Page Template Language - PTL.

PTL ist stored in files with ending ".ptl"; and py2exe can not find these files.

= Further possibilites =

The quixote-guys do recognize that. So there is qx_distutils, which creates an own build-class. But... py2exe also does this. So ... both do not work together. Maybe we should create some qx2exe_distutils....

= A Workaround =

PTL files can be converted into .py format so that they can be included in a py2exe app. Be sure not to call the quixote.enable_ptl() function anywhere in your app, or you'll cause problems with py2exe's import mechanism!

See 
http://mail.mems-exchange.org/pipermail/quixote-users/2005-January/004096.html
for more information.
