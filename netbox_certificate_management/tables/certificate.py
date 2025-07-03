from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from netbox_certificate_management.models import *
from adestis_netbox_applications import *
from netbox_certificate_management.models import Certificate

import django_tables2 as tables


class CertificateTable(NetBoxTable):
    status = ChoiceFieldColumn()
    
    certificate = tables.Column(
        linkify=True
    )

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    url = columns.MarkdownColumn(
        linkify=True
    )
    
    installedapplication = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Certificate
        fields = ['name', 'status', 'tenant', 'version', 'description', 'tags', 'tenant_group', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'comments', 'installedapplication']
        default_columns = [ 'name', 'tenant', 'status' ]
        