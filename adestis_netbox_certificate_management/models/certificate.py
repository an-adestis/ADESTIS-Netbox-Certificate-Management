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

__all__ = (
    'CertificateStatusChoices',
    'Certificate',
)

class CertificateStatusChoices(ChoiceSet):
    key = 'Certificates.status'

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_INACTIVE, 'Inactive', 'red'),
    ]
    
class Certificate(NetBoxModel):

    status = django_models.CharField(
        max_length=50,
        choices=CertificateStatusChoices,
        verbose_name='Status',
        help_text='Status'
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
        max_length=2000,
        verbose_name='Common Name',
        blank=True
    )
    
    supplier_product = django_models.CharField(
        max_length=2000,
        verbose_name='Supplier Product',
        blank=True
    )
    
    issuer = django_models.CharField(
        max_length=2000,
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
    
    subject_key_identifier = django_models.CharField(
        max_length=40,
        unique=True,
        null=False,
        blank=False
    )
    
    key_technology = django_models.CharField(
        max_length=2000,
        verbose_name='Key Technology',
        blank=True
    )
    
    subject_alternative_name = django_models.CharField(
        max_length=2000,
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
    
    certificate = django_models.CharField(
        verbose_name='Certificate',
        help_text='The certificate to be linked to the certificate chain',
        unique=True,
        max_length=10000,
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
    
    predecessor_certificate = django_models.ManyToManyField(
        'self',
        related_name = 'certificate',
        verbose_name='Predecessor Certificate',
        blank=True
    )
    
    successor_certificates = django_models.ManyToManyField(
        'self',
        related_name = 'certificate',
        verbose_name='Successor Certificate',
        blank=True
    )
    
    class Meta:
        verbose_name_plural = "Certificates"
        verbose_name = 'Certificate'

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
        

 