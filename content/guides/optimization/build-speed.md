# Build speed

## Situation

py2exe-ing larger projects take some time for byte compilation.

## Solution

[psyco](http://psyco.sourceforge.net) can help both the compilation, and the
final program.
as Armin Rigo writes... "Psyco is a Python extension module which can massively
speed up the execution of any Python code."

## Example

To speed up [py2exe](../../getting-started/overview.md) insert at the top of
setup.py:

```python
import psyco
psyco.full()
```

and it will compile 2-20 times faster (depending on your code). This can also
improve your programs running speed if you insert it in top of the main module.

To generate a log of the process (there is no need to with
[py2exe](../../getting-started/overview.md), but you might want to for your
code) simply insert the line "psyco.log()" in-between the two others.
