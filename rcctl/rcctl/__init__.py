# -----------------------------------------------------------------------------
# Adapted from Microsoft OSS
# see https://github.com/Microsoft/service-fabric-cli
# -----------------------------------------------------------------------------

"""Azure Service Fabric Reliable Collection command line environment for querying.

This package contains the following exports:
launch -- main entry point for the command line environment
"""

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from rcctl.entry import launch
