#!/usr/bin/env python3
"""TODO: Put module docstring HERE.
"""

#==============================================================================
# Copyright (C) 2020 Ljubomir Kurij <kurijlj@gmail.com>
#
# This file is part of mda (Measurement Data Analytics).
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option)
# any later version.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
#==============================================================================


#==============================================================================
#
# This program uses code from Qt for Python examples of the Qt Toolkit
# <https://doc.qt.io/qtforpython/_downloads/06ada84b04e72c9468651471cc91b026/
# datavisualize.tar.bz2> by The Qt Company Ltd., available under a
# 3-Clause BSD License.
#
# 2020-09-19 Ljubomir Kurij <kurijlj@gmail.com>
#
# * mda.py: created.
#
#==============================================================================


# ============================================================================
#
# TODO:
# 
# * Refactor CommandLineApp class to take fewer attributes. Refactor __init__
#   to take only two arguments a program name and an app documentation, where
#   app documentation would be passed and stored as named touple.
#
#
# ============================================================================


# ============================================================================
#
# References (this section should be deleted in the release version)
#
#
# ============================================================================


# =============================================================================
# Modules import section
# =============================================================================

import argparse
import actions


# =============================================================================
# Global constants
# =============================================================================


#==============================================================================
# Utility classes and functions
#==============================================================================

def _format_epilog(epilog_addition, bug_mail):
    """Formatter for generating help epilogue text. Help epilogue text is an
    additional description of the program that is displayed after the
    description of the arguments. Usually it consists only of line informing
    to which email address to report bugs to, or it can be completely
    omitted.

    Depending on provided parameters function will properly format epilogue
    text and return string containing formatted text. If none of the
    parameters are supplied the function will return None which is default
    value for epilog parameter when constructing parser object.
    """

    fmt_mail = None
    fmt_eplg = None

    if epilog_addition is None and bug_mail is None:
        return None

    if bug_mail is not None:
        fmt_mail = 'Report bugs to <{bug_mail}>.'\
            .format(bug_mail = bug_mail)
    else:
        fmt_mail = None

    if epilog_addition is None:
        fmt_eplg = fmt_mail

    elif fmt_mail is None:
        fmt_eplg = epilog_addition

    else:
        fmt_eplg = '{addition}\n\n{mail}'\
            .format(addition = epilog_addition, mail = fmt_mail)

    return fmt_eplg


def _formulate_action(action, **kwargs):
    """Factory method to create and return proper action object.
    """

    return action(**kwargs)


#==============================================================================
# Command line app class
#==============================================================================

class CommandLineApp():
    """Actual command line app object containing all relevant application
    information (NAME, VERSION, DESCRIPTION, ...) and which instantiates
    action that will be executed depending on the user input from
    command line.
    """

    def __init__(self,
        program_name=None,
        program_description=None,
        program_license=None,
        version_string=None,
        year_string=None,
        author_name=None,
        author_mail=None,
        epilog=None):

        self.program_license = program_license
        self.version_string = version_string
        self.year_string = year_string
        self.author_name = author_name
        self.author_mail = author_mail

        fmt_eplg = _format_epilog(epilog, author_mail)

        self._parser = argparse.ArgumentParser(
            prog = program_name,
            description = program_description,
            epilog = fmt_eplg,
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

        # Since we add argument options to groups by calling group
        # method add_argument, we have to sore all that group objects
        # somewhere before adding arguments. Since we want to store all
        # application relevant data in our application object we use
        # this list for that purpose.
        self._arg_groups = []

        self._action = None


    @property
    def program_name(self):
        """Utility function that makes accessing program name attribute
        neat and hides implementation details.
        """
        return self._parser.prog


    @property
    def program_description(self):
        """Utility function that makes accessing program description
        attribute neat and hides implementation details.
        """
        return self._parser.description


    def add_argument_group(self, title=None, description=None):
        """Adds an argument group to application object.
        At least group title must be provided or method will rise
        NameError exception. This is to prevent creation of titleless
        and descriptionless argument groups. Although this is allowed bu
        argparse module I don't see any use of a such utility."""

        if title is None:
            raise NameError('Missing arguments group title.')

        group = self._parser.add_argument_group(title, description)
        self._arg_groups.append(group)

        return group


    def _group_by_title(self, title):
        group = None

        for item in self._arg_groups:
            if title == item.title:
                group = item
                break

        return group


    def add_argument(self, *args, **kwargs):
        """Wrapper for add_argument methods of argparse module. If
        parameter group is supplied with valid group name, argument will
        be added to that group. If group parameter is omitted argument
        will be added to parser object. In a case of invalid group name
        it rises ValueError exception.
        """

        if 'group' not in kwargs or kwargs['group'] is None:
            self._parser.add_argument(*args, **kwargs)

        else:
            group = self._group_by_title(kwargs['group'])

            if group is None:
                raise ValueError(
                'Trying to reference nonexisten argument group.'
                )

            kwargsr = {k:kwargs[k] for k in kwargs if k != 'group'}
            group.add_argument( *args, **kwargsr)


    def parse_args(self, args=None, namespace=None):
        """Wrapper for parse_args method of a parser object. It also
        instantiates action object that will be executed based on a
        input from command line.
        """

        arguments = self._parser.parse_args(args, namespace)

        if arguments.usage:
            self._action = _formulate_action(
                actions.ProgramUsageAction,
                parser=self._parser,
                exitf=self._parser.exit)

        elif arguments.version:
            self._action = _formulate_action(
                actions.ShowVersionAction,
                prog=self._parser.prog,
                ver=self.version_string,
                year=self.year_string,
                author=self.author_name,
                license=self.program_license,
                exitf=self._parser.exit)

        else:
            self._action = _formulate_action(
                actions.DefaultAction,
                prog=self._parser.prog,
                exitf=self._parser.exit)


    def run(self):
        """This method executes action code.
        """

        self._action.execute()


#==============================================================================
# Script main body
#==============================================================================

if __name__ == '__main__':
    PROGRAM_DESCRIPTION='\
CLI application development for Python implementing argp option parsing \
engine.\n\
Mandatory arguments to long options are mandatory for short options too.'
    PROGRAM_LICENSE='\
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\
\n\
This is free software: you are free to change and redistribute it.\n\
There is NO WARRANTY, to the extent permitted by law.'

    program = CommandLineApp(
        program_description=PROGRAM_DESCRIPTION.replace('\t', ''),
        program_license=PROGRAM_LICENSE.replace('\t', ''),
        version_string='i.i',
        year_string='yyyy',
        author_name='Author Name',
        author_mail='author@mail.com',
        epilog=None
        )

    program.add_argument_group('general options')
    program.add_argument(
        '-V', '--version',
        action='store_true',
        help='print program version',
        group='general options'
        )
    program.add_argument(
        '--usage',
        action='store_true',
        help='give a short usage message'
        )

    program.parse_args()
    program.run()
