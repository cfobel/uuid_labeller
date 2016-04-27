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

The date or date/time combination can also be inserted with `{{date}}` and `{{datetime}}`, respectively.

Generated UUIDs can be saved to a .csv file and will be appended to an existing file.
Each per-instance UUID will generate a row with either a single column if no global UUID exists, or the global UUID in the first column and the per-instance UUID in the second.

Installation
------------

### Windows ###

Copy `uuid_labeller.py` and `uuid_labeller.inx` to the following directory:

    C:\Users\<user>\AppData\Roaming\inkscape\extensions

### Linux (and OS X?) ###

Copy `uuid_labeller.py` and `uuid_labeller.inx` to the following directory:

    ~/.config/inkscape/extensions


Usage
-----

### Basic usage ###

![usage][usage-pic]

### Slice notation ###

![usage-slice][usage-slice-pic]


Credits
-------

Copyright 2016 Christian Fobel and Michael Dryden


[usage-pic]: docs/usage.gif
[usage-slice-pic]: docs/usage-slice.gif
