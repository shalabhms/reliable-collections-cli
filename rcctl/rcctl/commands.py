# -----------------------------------------------------------------------------
# Adapted from Microsoft OSS
# see https://github.com/Microsoft/service-fabric-cli
# -----------------------------------------------------------------------------

"""Command and help loader for the Service Fabric CLI.

Commands are stored as one to one mappings between command line syntax and
python function.
"""

from collections import OrderedDict
from knack.arguments import ArgumentsContext
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
            with super_group.group('dictionary') as group:
                group.command('query', 'query_reliabledictionary')
                group.command('execute', 'execute_reliabledictionary')
                group.command('schema', 'get_reliabledictionary_schema')
                group.command('list', 'get_reliabledictionary_list')
                group.command('type-schema', 'get_reliabledictionary_type_schema')

        with ArgumentsContext(self, 'dictionary') as ac:
            ac.argument('application_name', options_list=['--application-name', '-a'])
            ac.argument('service_name', options_list=['--service-name', '-s'])
            ac.argument('dictionary_name', options_list=['--dictionary-name', '-d'])
            ac.argument('output_file', options_list=['--output-file', '-out'])
            ac.argument('input_file', options_list=['--input-file', '-in'])
            ac.argument('query_string', options_list=['--query-string', '-q'])
            ac.argument('type_name', options_list=['--type-name', '-t'])
        
        return OrderedDict(self.command_table)