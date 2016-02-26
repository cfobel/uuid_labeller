uuid_labeller
=============

An Inkscape plugin to replace template tags with UUID labels.


Overview
--------

This Inkscape plugin replaces text in an SVG in the form `{{ my_label }}` with
a UUID.

If tag name is surrounded by angle brackets, e.g., `{{ <my_label> }}`, a unique
UUID tag is assigned to each occurrence. Otherwise, the same UUID tag is
assigned to all occurrences of each label.

Slice notation can be used in the extension dialog to only replace with a
substring of the UUID.


Usage
-----

### Basic usage ###

![usage][usage-pic]

### Slice notation ###

![usage-slice][usage-slice-pic]


Credits
-------

Copyright 2016 Christian Fobel


[usage-pic]: docs/usage.gif
[usage-slice-pic]: docs/usage-slice.gif
