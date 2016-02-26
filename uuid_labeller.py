#!/usr/bin/env python

import re
# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')
from uuid import uuid4

# We will use the inkex module with the predefined Effect base class.
import inkex
# The simplestyle module provides functions for style parsing.
from simplestyle import *


# Regex to match a pattern entered in the extension parameters dialog.
cre_pattern = re.compile(r'(?P<pattern>(?P<multi><\w+>)|\w+)(\[(?P<start>-?\d+)?:?(?P<end>-?\d+)\])?')


class UUIDLabelEffect(inkex.Effect):
    """
    Replace template tags with UUID labels.
    """
    def __init__(self):
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-t', '--tags', action='store',
                                     type='string', dest='tags',
                                     default='', help='Comma separated UUID '
                                     'replacement tags.')

    def effect(self):
        """
        Replace text in the form `{{ my_label }}` with a UUID.

        If label name is surrounded by angle brackets, e.g.,
        `{{ <my_label> }}`, a unique UUID tag is assigned to each occurrence.
        Otherwise, the same UUID tag is assigned to all occurrences of each label.

        Slice notation can be used in the extension dialog to only replace with
        a substring of the UUID.
        """
        # Get script's "--tags" option value.
        tags = self.options.tags

        for pattern in [v.strip() for v in tags.split(',')
                        if v.strip()]:
            uuid = str(uuid4())
            match = cre_pattern.match(pattern)
            if not match:
                continue
            pattern_attrs = match.groupdict()
            for element_i in self.document.xpath('//svg:text[contains(text(), '
                                                 '"%s")]' %
                                                 pattern_attrs['pattern'],
                                                 namespaces=inkex.NSS):
                text_i = element_i.text
                if pattern_attrs['multi'] is not None:
                    uuid_i = str(uuid4())
                else:
                    uuid_i = uuid
                start = (0 if pattern_attrs['start'] is None else
                         int(pattern_attrs['start']))
                end = (len(uuid_i) if pattern_attrs['end'] is None else
                       int(pattern_attrs['end']))
                text_i = re.sub(r'{{\s*%s\s*}}' % pattern_attrs['pattern'],
                                uuid_i[start:end], text_i)
                element_i.text = text_i


# Create effect instance and apply it.
effect = UUIDLabelEffect()
effect.affect()