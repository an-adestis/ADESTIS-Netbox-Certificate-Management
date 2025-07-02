from rest_framework import serializers
from netbox_cars.models import *
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.models import *
from tenancy.api.serializers import *
from dcim.api.serializers import *
from dcim.models import *
from virtualization.api.serializers import *

class CarsSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_cars-api:cars-detail'
    )

    class Meta:
        model = Cars
        fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'created', 'last_updated',
                  'custom_field_data', 'status', 'comments', 'tenant', 'tenant_group', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'description', 'version')
        brief_fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'created', 'last_updated',
                        'custom_field_data', 'status', 'comments', 'tenant', 'tenant_group', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'description', 'version')

