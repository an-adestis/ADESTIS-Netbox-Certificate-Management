from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from netbox_cars.models import *
from adestis_netbox_applications import *
from netbox_cars.models import Cars
from netbox_cars.filtersets import *
import django_tables2 as tables


class CarsTable(NetBoxTable):
    status = ChoiceFieldColumn()
    
    cars = tables.Column(
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
        model = Cars
        fields = ['name', 'status', 'tenant', 'version', 'url', 'description', 'tags', 'tenant_group', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'comments', 'installedapplication']
        default_columns = [ 'name', 'tenant', 'version', 'status' ]
        