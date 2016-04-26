#!/usr/bin/env python

import re
from datetime import datetime
from os.path import expanduser
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
cre_pattern = re.compile(r'(?P<pattern>(?P<multi><\w+>)|(?P<date>date(?!time))|(?P<datetime>datetime)|\w+)(\[(?P<start>-?\d+)?:?(?P<end>-?\d+)\])?')


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
        self.OptionParser.add_option('-s', '--save_true', action='store',
                                     dest='save_true',
                                     default='', help='Save tags to file.')
        self.OptionParser.add_option('-p', '--path', action='store',
                                     type='string', dest='path',
                                     default='~/Desktop/tags.txt',
                                     help='Path to save tags.')

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
        save_true = self.options.save_true.lower()
        path = expanduser(self.options.path)
        uuid = str(uuid4())
        multi_uuids = []

        for pattern in [v.strip() for v in tags.split(',')
                        if v.strip()]:

            match = cre_pattern.match(pattern)
            if not match:
                continue
            pattern_attrs = match.groupdict()
            start = (0 if pattern_attrs['start'] is None else
                     int(pattern_attrs['start']))
            end = (len(uuid_i) if pattern_attrs['end'] is None else
                   int(pattern_attrs['end']))
            # Match text elements and all descendant elements of text elements
            # (e.g., `<span>`) containing pattern.
            xpath_str = ("(//svg:text |"
                         " //svg:text//svg:*)[contains(text(), '%s')]" %
                         pattern_attrs['pattern'])
    	    matches = self.document.xpath(xpath_str, namespaces=inkex.NSS)
            for element_i in matches:
                text_i = element_i.text
                if pattern_attrs['multi'] is not None:
                    uuid_i = str(uuid4())
                    multi_uuids.append(uuid_i[start:end])
                elif pattern_attrs['datetime'] is not None:
                    uuid_i = datetime.today().strftime('%Y-%m-%d %H:%M')
                elif pattern_attrs['date'] is not None:
                    uuid_i = datetime.today().strftime('%Y-%m-%d')
                else:
                    uuid_i = uuid

                text_i = re.sub(r'{{\s*%s\s*}}' % pattern_attrs['pattern'],
                                uuid_i[start:end], text_i)
                element_i.text = text_i
            
            if save_true == 'true':
                with open(path, 'a') as f:
                    for i in multi_uuids:
                        f.write('%s,%s\n' % (uuid[start:end], i))


# Create effect instance and apply it.
effect = UUIDLabelEffect()
effect.affect()
