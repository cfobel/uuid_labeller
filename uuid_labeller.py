#!/usr/bin/env python

from datetime import datetime
import os
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
cre_pattern = re.compile(r'(?P<pattern>('
                         r'(?P<datetime>datetime)|'
                         r'(?P<date>date(?!time))|'
                         r'(?P<global_label>\w+)|'
                         r'(?P<unique><(?P<unique_label>\w+)>)))'
                         r'(\[(?P<start>-?\d+)?:?(?P<end>-?\d+)\])?')


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
                                     default='~/Desktop/tags.csv',
                                     help='Path to save tags.')

    def effect(self):
        """
        Replace text in the form `{{ ... }}` with dynamic content (where `...`
        is a placeholder for user-specified text).

        Note that in all cases, `...` represents a placeholder for a
        user-specified text label.

         - Replace all occurrences of `{{ date }}` with `<year>-<month>-<day>`.
         - Replace all occurrences of `{{ datetime }}` with
           `<year>-<month>-<day> <hour>-<minute>`.
         - Replace all occurrences of `{{ ... }}` with the same UUID.
         - Replace each occurrence of `{{ <...> }}` with a unique UUID.

        ### Note ###

        Each placeholder label (i.e., `...` placeholder text) is assigned a
        *global* UUID.  Document text in the form `{{ ... }}` is replaced with
        the *global* UUID of the corresponding label.  Each occurrence of
        document text in the form `{{ <...> }}` is replaced with a unique UUID,
        but the *global* UUID for the corresponding `...` label is included
        when writing to the save path.

        For UUID placeholders (i.e., `{{ <...> }}` or `{{ ... }}` ), slice
        notation can be used in the extension dialog to only replace with
        a substring of the UUID (e.g., `<...>[1:3],...[:-10]`).

        Examples
        --------

        Consider an Inkscape SVG document containing text elements with the
        following content:

            {{ batch }}#{{ <batch> }}
            {{ batch }}#{{ <batch> }}
            {{ batch }}#{{ <batch> }}
            {{ datetime }}
            {{ date }}

        Assume the UUID labeller extension is applied with the following
        setting:

            batch[:6],<batch>[:8],datetime,date

        The resulting contents of the text elements would be similar to:

            9c767f#c36830b7
            9c767f#86b6ed72
            9c767f#ecd4916f
            2016-04-27 11:39
            2016-04-27
        """
        # Get script's "--tags" option value.
        tags = self.options.tags
        save_true = self.options.save_true.lower()
        path = os.path.expanduser(self.options.path)
        global_uuids = {}  # Global UUID for each label
        unique_uuids = {}  # List of unique UUIDs for each label

        def get_global_uuid(label):
            if label not in global_uuids:
                uuid = str(uuid4())
                # Record UUID for label.
                global_uuids[label] = uuid
                # Initialize empty unique UUIDs list for label.
                unique_uuids[label] = []
            else:
                # Reuse existing global UUID for label.
                uuid = global_uuids[label]
            return uuid

        for pattern in [v.strip() for v in tags.split(',') if v.strip()]:
            # Each `pattern` is in one of the following forms:
            #  - `...` (common UUID for all occurrences)
            #  - `<...>` (`unique` key: multiple unique UUIDs)
            #  - `date` (`date` key: date string)
            #  - `datetime` (`datetime` key: date and  time string)
            #
            # UUID patterns may have optional slice notation suffix
            # (e.g., `[:8]`).

            match = cre_pattern.match(pattern)
            if not match:
                continue
            pattern_attrs = match.groupdict()

            start = (0 if pattern_attrs['start'] is None else
                     int(pattern_attrs['start']))
            end = (None if pattern_attrs['end'] is None else
                   int(pattern_attrs['end']))

            # Match text elements and all descendant elements of text elements
            # (e.g., `<span>`) containing pattern.
            xpath_str = ("(//svg:text |"
                         " //svg:text//svg:*)[contains(text(), '%s')]" %
                         pattern_attrs['pattern'])
    	    matches = self.document.xpath(xpath_str, namespaces=inkex.NSS)
            for element_i in matches:
                text_i = element_i.text

                for k in ['global_label', 'unique_label']:
                    label_i = pattern_attrs[k]
                    if label_i is not None:
                        # Get global UUID pattern to associate with all all
                        # occurrences of label.
                        global_uuid_i = get_global_uuid(label_i)
                        if k == 'global_label':
                            # Replace all occurrences of pattern with global
                            # UUID for label.
                            uuid_i = global_uuid_i
                        else:
                            # Replace each occurrences of pattern with unique
                            # UUID.
                            uuid_i = str(uuid4())
                            unique_uuids[label_i].append(uuid_i)

                if pattern_attrs['datetime'] is not None:
                    uuid_i = datetime.today().strftime('%Y-%m-%d %H:%M')
                elif pattern_attrs['date'] is not None:
                    uuid_i = datetime.today().strftime('%Y-%m-%d')

                text_i = re.sub(r'{{\s*%s\s*}}' % pattern_attrs['pattern'],
                                uuid_i[start:end], text_i)
                element_i.text = text_i

        if save_true == 'true':
            if not os.path.exists(path) or os.stat(path).st_size == 0:
                # File doesn't exist yet or is empty, so write header row.
                with open(path, 'a') as f:
                    f.write('utctimestamp,label,global_uuid,uuid\n')

            utctimestamp = datetime.utcnow().isoformat()
            with open(path, 'a') as f:
                for label_i, unique_uuids_i in unique_uuids.iteritems():
                    global_uuid_i = global_uuids[label_i]
                    global_prefix_i = '%s' % ','.join([utctimestamp, label_i,
                                                       global_uuid_i])
                    if not unique_uuids_i:
                        # There were no unique UUIDs for the associated label.
                        # Write the global UUID for the label.
                        f.write('%s,\n' % global_prefix_i)
                    else:
                        # Write a new line for each unique UUID with the same
                        # label.
                        for uuid_j in unique_uuids_i:
                            f.write('%s\n' % ','.join((global_prefix_i,
                                                       uuid_j)))


# Create effect instance and apply it.
effect = UUIDLabelEffect()
effect.affect()
