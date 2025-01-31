from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_certificate_management.models import *


class CertificateTable(NetBoxTable):
    status = ChoiceFieldColumn()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()


    class Meta(NetBoxTable.Meta):
        model = Certificate
        fields = ['pk', 'id', 'status', 'comments', 'actions', 'tags', 'created', 'last_updated']
        default_columns = ['pk', 'id', 'status', 'comments', 'actions', 'tags', 'created', 'last_updated']
