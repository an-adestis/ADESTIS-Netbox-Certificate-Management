from rest_framework import serializers
from adestis_netbox_certificate_management.models import *
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.models import *
from tenancy.api.serializers import *
from dcim.api.serializers import *
from dcim.models import *
from virtualization.api.serializers import *

class CertificateSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_certificate_management-api:certificate-detail'
    )

    class Meta:
        model = Certificate
        fields = ('id', 'tags', 'custom_fields', 'display', 'created', 'last_updated',
                  'custom_field_data', 'status', 'comments', 'tenant', 'tenant_group', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'description')
        brief_fields = ('id', 'tags', 'custom_fields', 'display', 'created', 'last_updated',
                        'custom_field_data', 'status', 'comments', 'tenant', 'tenant_group', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'description')

