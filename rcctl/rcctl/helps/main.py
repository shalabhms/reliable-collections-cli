# -----------------------------------------------------------------------------
# Adapted from Microsoft OSS
# see https://github.com/Microsoft/service-fabric-cli
# -----------------------------------------------------------------------------

"""Help documentation for Reliable Collection groups"""

from knack.help_files import helps

helps[''] = """
    type: group
    short-summary: Commands for managing Service Fabric reliable collections.
    long-summary: Commands follow the noun-verb pattern. See subgroups for more
        information.
"""

helps['cluster'] = """
    type: group
    short-summary: Select a Service Fabric cluster to operate against. Defaults to http://localhost:19080/
"""

helps['dictionary'] = """
    type: group
    short-summary: Query and perform operations on IReliableDictionaries
"""
