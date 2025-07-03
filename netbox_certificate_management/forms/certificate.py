from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from netbox_certificate_management.models.certificate import Certificate, CertificateStatusChoices
from adestis_netbox_applications.models import *
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
from utilities.forms import ConfirmationForm

__all__ = (
    'CertificateForm',
    'CertificateFilterForm',
    'CertificateBulkEditForm',
    'CertificateCSVForm',
    'CertificateCRTForm',
    'CertificateAssignApplicationForm',
    'CertificateRemoveApplication'
)

class CertificateCRTForm(forms.Form):
    
    certificate = forms.FileField(
        # widget=forms.FileInput(attrs={'multiple': True}),
        label='Certificate',
        required=True,
    )
    
    status = forms.ChoiceField(
        required=False,
        label='Status',
        choices=CertificateStatusChoices,
    )
    
    class Meta:
        model = Certificate
        fields = ['name', 'valid_from', 'valid_to', 'contact_group',  'subject', 'subject_alternative_name','issuer_parent_certificate', 'key_technology',  'issuer', 'certificate', 'tags']
        default_return_url = 'plugins:netbox_certificate_management:certificate_list'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the `multiple` attribute to allow selecting multiple files
        self.fields["certificate"].widget.attrs.update({"multiple": "true"})

class CertificateForm(NetBoxModelForm):

    fieldsets = (
        FieldSet('name', 'description', 'tags', 'status', name=_('Certificate')),
        FieldSet('tenant_group', 'tenant',  name=_('Tenant')), 
        FieldSet('cluster', 'cluster_group', 'virtual_machine', name=_('Virtualization')),   
        FieldSet('device', name=_('Device')),
        FieldSet('installedapplication', name=_('Application'))
    )

    class Meta:
        model = Certificate
        fields = ['name', 'description', 'tags', 'status', 'tenant', 'tenant_group', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'comments', 'installedapplication']
        
        help_texts = {
            'status': "Example text",
        }

class CertificateBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Certificate.objects.all(),
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
    

    status = forms.ChoiceField(
        required=False,
        choices=CertificateStatusChoices,
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
    
    model = Certificate

    fieldsets = (
        FieldSet('name', 'description', 'tags', 'status', 'comments', name=_('Application')),
        FieldSet('tenant_group', 'tenant', name=_('Tenant')),
        FieldSet('cluster', 'cluster_group', 'virtual_machine', name=_('Virtualization')),
        FieldSet('device', name=_('Device'))
    )

    nullable_fields = [
         'add_tags', 'remove_tags', 'description', ''
    ]
    
class CertificateFilterForm(NetBoxModelFilterSetForm):
    
    model = Certificate

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'tag', 'status', name=_('Application')),
        FieldSet('tenant_group_id', 'tenant_id', name=_('Tenant')),
        FieldSet('cluster_id', 'cluster_group_id', 'virtual_machine_id', name=_('Virtualization')),
        FieldSet('device_id', name=_('Device'))
    )

    index = forms.IntegerField(
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=CertificateStatusChoices,
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

    
class CertificateCSVForm(NetBoxModelImportForm):

    status = CSVChoiceField(
        choices=CertificateStatusChoices,
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
        model = Certificate
        fields = ['name' ,'status', 'tenant', 'tenant_group', 'cluster', 'cluster_group', 'virtual_machine', 'device', 'description',  'tags', 'comments']
        default_return_url = 'plugins:netbox_certificate_management:Certificate_list'
        
class CertificateAssignApplicationForm(forms.Form):
    
    installedapplication = DynamicModelMultipleChoiceField(
        label=_('Applications'),
        queryset=InstalledApplication.objects.all()
    )

    class Meta:
        fields = [
            'installedapplication',
        ]

    def __init__(self, certificate, *args, **kwargs):

        self.certificate = certificate

        self.installedapplication = DynamicModelMultipleChoiceField(
            label=_('Applications'),
            queryset=InstalledApplication.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['installedapplication'].choices = []
        
class CertificateRemoveApplication(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=InstalledApplication.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    


    