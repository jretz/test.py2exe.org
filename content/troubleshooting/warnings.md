# Dealing With Warnings resulting in Application Fatal Errors in windows mode

When warnings are emitted in windows mode (no console available) the warning
messages can't be correctly output and the application exits with an error
message. This problem doesn't usually interfere with the application features,
but it's very inconvenient and ugly.

To filter out warnings and avoid the problem, you can use the `warnings` module,
part of the Python standard library.

It allows suppressing warnings like this:

```python2
import warnings
warnings.simplefilter('ignore')
```

See [the warnings module in the stdlib][link-1] for more options.

[link-1]: http://docs.python.org/library/warnings.html
