# Quixote

## The Problem

Quixote may use a Page Template Language - PTL.

PTL ist stored in files with ending ".ptl"; and py2exe can not find these files.

## Further possibilites

The quixote-guys do recognize that. So there is qx\_distutils, which creates an
own build-class. But... py2exe also does this. So ... both do not work together.
Maybe we should create some qx2exe\_distutils....

## A Workaround

PTL files can be converted into .py format so that they can be included in a
py2exe app. Be sure not to call the quixote.enable\_ptl() function anywhere in
your app, or you'll cause problems with py2exe's import mechanism!

See
<http://mail.mems-exchange.org/quixote-users/4096/>
for more information.
