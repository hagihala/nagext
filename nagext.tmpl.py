# Copyright 2010 Alexander Duryagin
#
# This file is part of NagExt.
#
# NagExt is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NagExt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NagExt.  If not, see <http://www.gnu.org/licenses/>.
#

"""
This module provides python interface to Nagios external commands
"""

from time import time

class ExecError(Exception):
    """
    Errors while executing command (writing external command to command file)
    """
    pass

class NagExt(object):
    """
    Deal with nagios command file for executing external commands.
    Writes commands to Nagios command_file in following format:
    [time] command_id;command_arguments

    """

    def __init__(self, command_file):
        self.command_file = command_file
        self._cmd_f = None
        self.open()
    
    def __del__(self):
        self.close()

    def open(self):
        """
        Open Nagios command file
        """
        self._cmd_f = open(self.command_file, 'w')
    
    def close(self):
        """
        Close Nagios command file
        """
        self._cmd_f.close()

    def run(self, cmd, *args):
    	"""
        Run Nagios external command with given arguments, converting bool to int
        """
        def bool2int(a):
            if isinstance(a, bool):
                return int(a)
            else:
                return a
        try:
            str_args = ';'.join([ str(bool2int(a)) for a in args ])
            print >> self._cmd_f, "[%lu] %s;%s" % (time(), cmd, str_args)
        except Exception, e:
            raise ExecError(str(e))

    # next follow automatically generated methods from nagios developer documentation
    # for external commands

