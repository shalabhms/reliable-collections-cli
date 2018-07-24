# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric groups"""

from knack.help_files import helps

helps[''] = """
    type: group
    short-summary: Commands for managing Service Fabric reliable collections.
    long-summary: Commands follow the noun-verb pattern. See subgroups for more
        information.
"""

helps['cluster'] = """
    type: group
    short-summary: Select, manage and operate Service Fabric clusters
"""

helps['collections'] = """
    type: group
    short-summary: Query and perform operations on reliable collections
"""
