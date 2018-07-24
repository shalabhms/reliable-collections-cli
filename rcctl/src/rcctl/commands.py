# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Command and help loader for the Service Fabric CLI.

Commands are stored as one to one mappings between command line syntax and
python function.
"""

from collections import OrderedDict
from knack.commands import CLICommandsLoader, CommandSuperGroup
from knack.help import CLIHelp
from rcctl.apiclient import create as client_create

# Need to import so global help dict gets updated
import rcctl.helps.main # pylint: disable=unused-import

class SFCommandHelp(CLIHelp):
    """Service Fabric CLI help loader"""

    def __init__(self, ctx=None):
        header_msg = 'Service Fabric Command Line'

        super(SFCommandHelp, self).__init__(ctx=ctx,
                                            welcome_message=header_msg)

class SFCommandLoader(CLICommandsLoader):
    """Service Fabric CLI command loader, containing command mappings"""

    def load_command_table(self, args): #pylint: disable=too-many-statements
        """Load all Service Fabric commands"""

        # Need an empty client for the select and upload operations
        with CommandSuperGroup(__name__, self,
                               'rcctl.custom_cluster#{}') as super_group:
            with super_group.group('cluster') as group:
                group.command('select', 'select')

        with CommandSuperGroup(__name__, self, 'rcctl.custom_reliablecollections#{}',
                               client_factory=client_create) as super_group: 
            with super_group.group('collections') as group:
                group.command('query', 'query_reliablecollections')
                group.command('execute', 'execute_reliablecollections')
                group.command('schema', 'get_reliablecollections_schema')
                group.command('list', 'get_reliablecollections_list')
                group.command('type', 'get_reliablecollections_type')
        
        return OrderedDict(self.command_table)

    def load_arguments(self, command):
        """Load specialized arguments for commands"""
        from rcctl.params import custom_arguments

        custom_arguments(self, command)

        super(SFCommandLoader, self).load_arguments(command)
