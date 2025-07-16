from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_certificate_management.models import *
from adestis_netbox_applications import *
from adestis_netbox_certificate_management.models import Certificate

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
    
    valid_from = columns.DateColumn()
    
    valid_to = columns.DateColumn()
    
    tenant = tables.Column(
        linkify = True
    )
    
    tenant_group = tables.Column(
        linkify = True
    )

    description = columns.MarkdownColumn()
    
    url = columns.MarkdownColumn(
        linkify=True
    )
    
    installedapplication = tables.Column(
        linkify=True
    )
    
    contact = tables.Column(
        linkify=True
    )
    
    virtual_machine = tables.Column(
        linkify=True
    )
    
    cluster_group = tables.Column(
        linkify=True
    )
        
    cluster = tables.Column(
        linkify=True
    )
        
    device = tables.Column(
        linkify=True
    )
    
    predecessor_certificate = tables.Column(
        linkify=True
    )
    
    successor_certificates = tables.Column(
        linkify=True
    )
    
    issuer_parent_certificate = tables.Column(
        linkify=True
    )
    
    issuer = columns.MarkdownColumn(
    )
    
    authority_key_identifier = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Certificate
        fields = ['name', 'status',   'description', 'tags',  'comments', 'valid_from', 'valid_to', 'contact_group', 'issuer', 'authority_key_identifier', 'issuer_parent_certificate', 'subject', 'subject_alternative_name', 'key_technology', 'tenant', 'installedapplication', 'tenant_group', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'contact', 'successor_certificates', 'predecessor_certificate', 'certificate']
        default_columns = [ 'name', 'tenant', 'status', 'valid_from', 'valid_to', 'authority_key_identifier' ]
        