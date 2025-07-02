from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from netbox_cars.models.application import Cars, CarsStatusChoices
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from tenancy.models import Tenant, TenantGroup
from dcim.models import *
from virtualization.models import *

__all__ = (
    'CarsForm',
    'CarsFilterForm',
    'CarsBulkEditForm',
    'CarsCSVForm',
)

class CarsForm(NetBoxModelForm):

    fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status', 'version', name=_('Application')),
        FieldSet('tenant_group', 'tenant',  name=_('Tenant')), 
        FieldSet('manufacturer', 'cluster', 'cluster_group', 'virtual_machine', name=_('Virtualization')),   
        FieldSet('device', name=_('Device'))
    )

    class Meta:
        model = Cars
        fields = ['name', 'description', 'url', 'tags', 'status', 'tenant', 'tenant_group', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'comments', 'version']
        
        help_texts = {
            'status': "Example text",
        }

class CarsBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Cars.objects.all(),
        widget=forms.MultipleHiddenInput, 
    )
    
    name = forms.CharField(
        required=False,
        max_length = 150,
        label=_("Name"),
    )
    
    comments = forms.CharField(
        max_length=150,
        required=False,
        label=_("Comment")
    )
    
    url = forms.URLField(
        max_length=300,
        required=False,
        label=_("URL")
    )
    
    version = forms.CharField(
        max_length=200,
        required=False,
        label=_("Version")
    )

    status = forms.ChoiceField(
        required=False,
        choices=CarsStatusChoices,
    )
    
    description = forms.CharField(
        max_length=500,
        required=False,
        label=_("Description"),
    )
    
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required = False,
        label = ("Virtual Machines")
    )
    
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required = False,
        label =_("Device")
    )
    
    tenant_group = DynamicModelChoiceField(
        queryset=TenantGroup.objects.all(),
        required = False,
        label=_("Tenant Group"),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required = False,
        label=_("Tenant"),
    )
    
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required = False,
        label=_("Manufacturer")
    )
    
    cluster_group = DynamicModelChoiceField(
        queryset=ClusterGroup.objects.all(),
        required = False,
        label=_("Cluster Group")
    )
    
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required = False,
        label=_("Cluster")
    )
    
    model = Cars

    fieldsets = (
        FieldSet('name', 'description', 'url', 'tags', 'status', 'version', 'comments', name=_('Application')),
        FieldSet('tenant_group', 'tenant', name=_('Tenant')),
        FieldSet('manufacturer', 'cluster', 'cluster_group', 'virtual_machine', name=_('Virtualization')),
        FieldSet('device', name=_('Device'))
    )

    nullable_fields = [
         'add_tags', 'remove_tags', 'description', ''
    ]
    
class CarsFilterForm(NetBoxModelFilterSetForm):
    
    model = Cars

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'url', 'tag', 'status', name=_('Application')),
        FieldSet('tenant_group_id', 'tenant_id', name=_('Tenant')),
        FieldSet('manufacturer_id', 'cluster_id', 'cluster_group_id', 'virtual_machine_id', name=_('Virtualization')),
        FieldSet('device_id', name=_('Device'))
    )

    index = forms.IntegerField(
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=CarsStatusChoices,
        required=False,
        label=_('Status')
    )
    
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'cluster_id': '$cluster_id',
        },
        label=_('Device')
    )
    
    virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'cluster_id': '$cluster_id',
            'device_id': '$device_id',
        },
        label=_('Virtual Machine')
    )
    
    cluster_group_id = DynamicModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        null_option='None',
        label=_('Cluster Group')
    )

    cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'group_id': '$cluster_group_id'
        },
        label=_('Cluster')
    )
    
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        null_option='None',   
        label=_('Manufacturer')
    )
    
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'group_id': '$tenant_group_id'
        },
        label=_('Tenant')
    )
    
    tenant_group_id = DynamicModelChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        null_option='None',
        label=_('Tenant Group')
    )

    tag = TagFilterField(model)

    
class CarsCSVForm(NetBoxModelImportForm):

    status = CSVChoiceField(
        choices=CarsStatusChoices,
        help_text=_('Status'),
        required=True,
    )
    
    tenant_group = CSVModelChoiceField(
        label=_('Tenant Group'),
        queryset=TenantGroup.objects.all(),
        required=True,
        to_field_name='name',
        help_text=('Assigned tenant group')
    )
    
    tenant = CSVModelChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned tenant')
    )
    
    manufacturer = CSVModelChoiceField(
        label=_("Manufacturer"),
        queryset=Manufacturer.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned manufacturer')
    )
    
    cluster_group = CSVModelChoiceField(
        label=_('Cluster Group'),
        queryset=ClusterGroup.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned cluster group')
    )
    
    cluster = CSVModelChoiceField(
        label=_('Cluster'),
        queryset=Cluster.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned cluster')
    )
    
    virtual_machine = CSVModelChoiceField(
        label=_('Virtual Machine'),
        queryset=VirtualMachine.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned virtual machine')
    )
    
    device = CSVModelChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Assigned device')
    )

    class Meta:
        model = Cars
        fields = ['name' ,'status',  'url', 'tenant', 'tenant_group', 'manufacturer', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'description',  'tags', 'comments', 'version']
        default_return_url = 'plugins:netbox_cars:Cars_list'


    