from adestis_netbox_certificate_management.models.certificate import Certificate
from netbox.filtersets import NetBoxModelFilterSet

from adestis_netbox_applications.models import InstalledApplication
from django.db.models import Q
from django import forms
import django_filters
from utilities.forms.widgets import DatePicker
from django.utils.translation import gettext as _
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
)
import django_filters
from utilities.filters import TreeNodeMultipleChoiceFilter
from virtualization.models import Cluster, ClusterGroup, VirtualMachine
from tenancy.models import Contact, ContactGroup, Tenant, TenantGroup
from dcim.models import Device
from ipam.api.serializers import *
from ipam.api.field_serializers import *

__all__ = (
    'CertificateFilterSet',
)

class CertificateFilterSet(NetBoxModelFilterSet):
    
    valid_from = django_filters.DateFilter(
        required=False,
        widget=DatePicker
    )

    valid_to = django_filters.DateFilter(
        required=False,
        widget=DatePicker
    )
    
    subject= django_filters.CharFilter(
        required=False
    ) 
    
    key_technology = django_filters.CharFilter(
        required=False,
        method='filter_key_technology',
    )
    
    subject_alternative_name = django_filters.CharFilter(
        required=False,
        method='filter_subject_alternative_name'
    )
    
    issuer_parent_certificate = django_filters.ModelMultipleChoiceFilter(
        field_name='issuer',
        queryset=Certificate.objects.all()
    )
    
    predecessor_certificate = django_filters.ModelMultipleChoiceFilter(
        field_name='predecessor_certificate',
        queryset=Certificate.objects.all()
    )
    
    successor_certificates = django_filters.ModelMultipleChoiceFilter(
        field_name='successor_certificates',
        queryset=Certificate.objects.all()
    )
    
    virtual_machine = django_filters.ModelMultipleChoiceFilter(
        field_name='virtual_machine',
        queryset=VirtualMachine.objects.all()
    )
    
    cluster_group = django_filters.ModelMultipleChoiceFilter(
        field_name='cluster_group',
        queryset=ClusterGroup.objects.all()
    )
    
    cluster = django_filters.ModelMultipleChoiceFilter(
        field_name='cluster',
        queryset=Cluster.objects.all()
    )
    
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device',
        queryset=Device.objects.all()
    )
    
    contact = django_filters.ModelMultipleChoiceFilter(
        field_name='contact',
        queryset=Contact.objects.all()
    )
    
    installedapplication = django_filters.ModelMultipleChoiceFilter(
        field_name='installedapplication',
        queryset=InstalledApplication.objects.all()
    )
    
    contact_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ContactGroup.objects.all(),
        label=_('Supplier (ID)'),
    )
    
    contact_group = DynamicModelMultipleChoiceField(
        queryset=ContactGroup.objects.all(),
        required=False,
        null_option='None',
        label=_('Supplier')
    )
    
    # device = DynamicModelMultipleChoiceField(
    #     queryset=Device.objects.all(),
    #     required = False,
    #     label=_('Device (ID)'),
    # )
    
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label=_('Tenant (Name)'),
    )
    
    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant (ID)'),
    )
    
    issuer_parent_certificate= DynamicModelMultipleChoiceField(
        queryset=Certificate.objects.all(),
        required=False,
        label=_('Issuer (name)'),
    )
    
    tenant_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        label=_('Tenant Group (ID)'),
    )
    
    tenant_group = DynamicModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        label=_('Tenant Group (name)'),
    )
    class Meta:
        model = Certificate
        fields = ['id', 'status', 'name', 'valid_from', 'valid_to', 'tenant', 'tenant_group', 'virtual_machine', 'device', 'cluster', 'cluster_group', 'installedapplication', 'subject', 'issuer_parent_certificate', 'successor_certificates', 'predecessor_certificate', 'key_technology', 'subject_alternative_name', 'contact', 'contact_group']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter( Q(status__icontains=value) )
    
    def filter_subject_alternative_name(self, queryset, name, value):
        if not value.strip():
            return queryset.none()
        return queryset.filter(subject_alternative_name__icontains=value)
    
    def filter_key_technology(self, queryset, name, value):
        if not value.strip():
            return queryset.none()  
        return queryset.filter(key_technology__icontains=value)

