from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from core.choices import JobIntervalChoices
from utilities.choices import ChoiceSet
from tenancy.models import *
from dcim.models import *
from virtualization.models import *
from adestis_netbox_applications import *
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator, ValidationError
from django import forms
from django.utils.html import escape
from django.utils.safestring import mark_safe
from utilities.validators import validate_regex
from django.utils.translation import gettext_lazy as _
from netbox.models.features import CloningMixin, ExportTemplatesMixin
from netbox.models import ChangeLoggedModel
from extras.models import TaggedItem
from taggit.managers import TaggableManager

__all__ = (
    'CertificateStatusChoices',
    'Certificate',
    'FormatChoises',
)

class FormatChoises(ChoiceSet):
    key ='Certificates.format'
    
    SELECT_File = 'select'
    PFX_FILE = 'pfx'
    PEM_FILE = 'pem'
    
    
    CHOICES = [
        (SELECT_File, 'Select'),
        (PFX_FILE, 'PFX'),
        (PEM_FILE, 'PEM'),
    ]

class CertificateStatusChoices(ChoiceSet):
    key = 'Certificates.status'

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_INACTIVE, 'Inactive', 'red'),
    ]
    
class Certificate(CloningMixin, ExportTemplatesMixin, ChangeLoggedModel):

    status = django_models.CharField(
        max_length=50,
        choices=CertificateStatusChoices,
        verbose_name='Status',
        help_text='Status'
    )
    
    tags = TaggableManager(through=TaggedItem)
    
    format = django_models.CharField(
        max_length=50, 
        choices=FormatChoises,
        verbose_name=_('format'),
        default=FormatChoises.PFX_FILE,
        help_text='Format'
    )
    
    pfx_password = django_models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_('Password'),
    )

    comments = django_models.TextField(
        blank=True
    )
    
    name = django_models.CharField(
        max_length=150
    )
    
    description = django_models.CharField(
        max_length=500,
        blank = True
    )
    
    subject = django_models.CharField(
        max_length=512,
        verbose_name='Common Name',
        blank=True
    )
    
    supplier_product = django_models.CharField(
        max_length=512,
        verbose_name='Supplier Product',
        blank=True
    )
    
    issuer = django_models.CharField(
        max_length=512,
        verbose_name='Issuer',
        blank=True
    )
    
    issuer_parent_certificate = django_models.ForeignKey(
        'self',
        verbose_name='Issuer (Parent Certificate)',
        on_delete = django_models.CASCADE,
        null=True,
        related_name='issued_certificates'
    )
    
    authority_key_identifier = django_models.ForeignKey(
        'self',
        verbose_name='Parent Certificate',
        on_delete = django_models.CASCADE,
        null=True,
        blank=True,
        related_name='authority_certificates'
    )
    
    authority_identifier = django_models.CharField(
        max_length=512,
        unique=True,
        null=True,
        blank=True
    )
    
    subject_key_identifier = django_models.CharField(
        max_length=512,
        unique=True,
        null=False,
        blank=False
    )
    
    key_technology = django_models.CharField(
        max_length=512,
        verbose_name='Key Technology',
        blank=True,
        null=True
    )
    
    subject_alternative_name = django_models.CharField(
        max_length=512,
        verbose_name='Subject Alternative Names',
        blank=True,
        null=True
    )
    
    valid_from = django_models.DateField(
        null=True,
        blank=True,
        verbose_name='Valid from',
        help_text='Start of validity'
    )
    
    valid_to = django_models.DateField(
        null=True,
        blank=True,
        verbose_name='Valid to',
        help_text='End of validity'
    )
    
    contact_group = django_models.ForeignKey(
        to = 'tenancy.ContactGroup',
        on_delete = django_models.PROTECT,
        related_name='certificate',
        verbose_name='Supplier',
        blank = True,
        null = True,
    )
    
    certificate = django_models.TextField(
        verbose_name='Certificate',
        help_text='The certificate to be linked to the certificate chain',
    )
    
    virtual_machine = django_models.ManyToManyField(
        to='virtualization.VirtualMachine',
        related_name= 'certificate',
        verbose_name='Virtual Machines',
        blank = True
    )
    
    device = django_models.ManyToManyField(
        to = 'dcim.Device',
        related_name= 'certificate',
        verbose_name='Devices',
        blank = True
    )
    
    tenant = django_models.ForeignKey(
         to = 'tenancy.Tenant',
         on_delete = django_models.PROTECT,
         related_name = 'certificate',
         null = True,
         verbose_name='Tenant',
         blank = True
     )
    
    tenant_group = django_models.ForeignKey(
        to= 'tenancy.TenantGroup',
        on_delete= django_models.PROTECT,
        related_name='certificate_tenant_group',
        null = True,
        verbose_name= 'Tenant Group',
        blank = True
    )
    
    installedapplication = django_models.ManyToManyField(
        'adestis_netbox_applications.InstalledApplication',
        related_name='certificate',
        verbose_name='Applications',
        blank = True
    )
    
    contact = django_models.ManyToManyField(
        to = 'tenancy.Contact',
        related_name='certificate',
        verbose_name='Contacts',
        blank = True
    )
    
    cluster = django_models.ManyToManyField(
        to = 'virtualization.Cluster',
        related_name = 'certificate',
        verbose_name='Clusters',
        blank = True
    )
    
    cluster_group = django_models.ManyToManyField(
        to = 'virtualization.ClusterGroup',
        
        related_name = 'certificate',
        verbose_name='Cluster Groups',
        blank = True
    )
    
    # successor_certificates = django_models.ManyToOneField(
    #     'self',
        
    #     blank=True, 
    #     # related_name='successor_certificate',
    #     # on_delete=django_models.SET_NULL
    # )

    
    class Meta:
        verbose_name_plural = "Certificates"
        verbose_name = 'Certificate'
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_certificate_management:certificate', args=[self.pk])

    def get_status_color(self):
        return CertificateStatusChoices.colors.get(self.status)
    
    def save(self, *args, **kwargs):
        from adestis_netbox_certificate_management.jobs import CertificateMetadataExtractorJob
        CertificateMetadataExtractorJob.enqueue_once()
        return super().save(*args, **kwargs)

    def sync(self):
        from adestis_netbox_certificate_management.jobs import CertificateMetadataExtractorJob
        CertificateMetadataExtractorJob.enqueue()
        

    
