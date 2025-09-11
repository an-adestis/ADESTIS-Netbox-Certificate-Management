from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_certificate_management.models import *
from adestis_netbox_applications import *
from adestis_netbox_certificate_management.models import Certificate
from dcim.tables import DeviceTable
from tenancy.tables import ContactTable, ContactGroupTable, TenantTable
from virtualization.tables import VirtualMachineTable, ClusterTable, ClusterGroupTable
from adestis_netbox_certificate_management.models import *
import django_tables2 as tables


class CertificateTable(NetBoxTable):
    
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    status = ChoiceFieldColumn()
    
    certificate = tables.Column(
        linkify=True
    )

    comments = columns.MarkdownColumn()

    # tags = columns.TagColumn()
    
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
    
    # successor_certificates = tables.Column(
    #     linkify=True
    # )
    
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
        fields = ['name', 'status',   'description', 'tags',  'comments', 'valid_from', 'valid_to', 'contact_group', 'issuer', 'authority_key_identifier', 'issuer_parent_certificate', 'subject', 'subject_alternative_name', 'key_technology', 'tenant', 'installedapplication', 'tenant_group', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'contact', 'certificate', 'actions']
        default_columns = [ 'name', 'tenant', 'status', 'valid_from', 'valid_to', 'authority_key_identifier' ]
        

class DeviceTableCertificate(DeviceTable):
    actions = columns.ActionsColumn(
        actions=('edit',  ),
        split_actions= False
    )
    
    class Meta(DeviceTable.Meta):
        fields = (
            'pk', 'id', 'name', 'status', 'tenant', 'tenant_group', 'role', 'manufacturer', 'device_type',
            'serial', 'asset_tag', 'region', 'site_group', 'site', 'location', 'rack', 'parent_device',
            'device_bay_position', 'position', 'face', 'latitude', 'longitude', 'airflow', 'primary_ip', 'primary_ip4',
            'primary_ip6', 'oob_ip', 'cluster', 'virtual_chassis', 'vc_position', 'vc_priority', 'description',
            'config_template', 'comments', 'contacts', 'tags', 'created', 'last_updated', 'actions',
        )
        default_columns = (
            'pk', 'name', 'status', 'tenant', 'site', 'location', 'rack', 'role', 'manufacturer', 'device_type',
            'primary_ip',
        )
        
class ClusterTableCertificate(ClusterTable):
    actions = columns.ActionsColumn(
        actions=('edit', ),
    )
    
    class Meta(ClusterTable.Meta):
        fields = (
            'pk', 'id', 'name', 'type', 'group', 'status', 'tenant', 'tenant_group', 'scope', 'scope_type',
            'description', 'comments', 'device_count', 'vm_count', 'contacts', 'tags', 'created', 'last_updated', 'actions'
        )
        default_columns = ('pk', 'name', 'type', 'group', 'status', 'tenant', 'site', 'device_count', 'vm_count')
        
class ClusterGroupTableCertificate(ClusterGroupTable):
    actions = columns.ActionsColumn(
        actions=('edit', ),
    )
    class Meta(ClusterGroupTable.Meta):
        fields = (
            'pk', 'id', 'name', 'slug', 'cluster_count', 'description', 'contacts', 'tags', 'created', 'last_updated',
            'actions',
        )
        default_columns = ('pk', 'name', 'cluster_count', 'description')
        
class VirtualMachineTableCertificate(VirtualMachineTable):
    
    actions = columns.ActionsColumn(
        actions=('edit', ),
    )
    
    class Meta(VirtualMachineTable.Meta):
        fields = (
            'pk', 'id', 'name', 'status', 'site', 'cluster', 'device', 'role', 'tenant', 'tenant_group', 'vcpus',
            'memory', 'disk', 'primary_ip4', 'primary_ip6', 'primary_ip', 'description', 'comments', 'config_template',
            'serial', 'contacts', 'tags', 'created', 'last_updated', 'actions'
        )
        default_columns = (
            'pk', 'name', 'status', 'site', 'cluster', 'role', 'tenant', 'vcpus', 'memory', 'disk', 'primary_ip',
        )
        
class ContactTableCertificate(ContactTable):
    
    actions = columns.ActionsColumn(
        actions=('edit', ),
    )
    
    class Meta(ContactTable.Meta):
        fields = (
            'pk', 'name', 'groups', 'title', 'phone', 'email', 'address', 'link', 'description', 'comments',
            'assignment_count', 'tags', 'created', 'last_updated', 'actions'
        )
        default_columns = ('pk', 'name', 'groups', 'assignment_count', 'title', 'phone', 'email')
