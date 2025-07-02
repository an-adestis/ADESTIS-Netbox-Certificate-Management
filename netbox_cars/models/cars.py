from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *
from dcim.models import *
from virtualization.models import *

__all__ = (
    'CarsStatusChoices',
    'Cars',
)

class CarsStatusChoices(ChoiceSet):
    key = 'Carss.status'

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_INACTIVE, 'Inactive', 'red'),
    ]
    
class Cars(NetBoxModel):

    status = django_models.CharField(
        max_length=50,
        choices=CarsStatusChoices,
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
    
    url = django_models.URLField(
        max_length=300
    )
    
    version = django_models.CharField(
         max_length=200,
     )
    
    virtual_machine = django_models.ForeignKey(
          to='virtualization.VirtualMachine',
          on_delete = django_models.PROTECT,
          related_name= 'cars_virtual_machine',
          null=True,
          verbose_name='Virtual Machine',
          blank=True
    )
    
    device = django_models.ForeignKey(
        to = 'dcim.Device',
        on_delete = django_models.PROTECT,
        related_name= 'cars_device',
        null = True,
        verbose_name='Device',
        blank=True
    )
    
    tenant = django_models.ForeignKey(
         to = 'tenancy.Tenant',
         on_delete = django_models.PROTECT,
         related_name = 'cars_tenant',
         null = True,
         verbose_name='Tenant',
         blank=True
     )
    
    tenant_group = django_models.ForeignKey(
        to= 'tenancy.TenantGroup',
        on_delete= django_models.PROTECT,
        related_name='cars_tenant_group',
        null = True,
        verbose_name= 'Tenant Group',
        blank=True
    )
    
    manufacturer = django_models.ForeignKey(
        to= 'dcim.Manufacturer',
        on_delete= django_models.PROTECT,
        related_name= 'cars_manufacturer',
        null= True,
        verbose_name='Manufacturer',
        blank=True
    )
    
    cluster = django_models.ForeignKey(
        to = 'virtualization.Cluster',
        on_delete = django_models.PROTECT,
        related_name = 'cars_cluster',
        null = True,
        verbose_name='Cluster',
        blank=True
    )
    
    cluster_group = django_models.ForeignKey(
        to = 'virtualization.ClusterGroup',
        on_delete = django_models.PROTECT,
        related_name = 'cars_cluster_group',
        null = True,
        verbose_name='Cluster Group',
        blank=True
    )
    
    installedapplication = django_models.ManyToManyField(
        'adestis_netbox_applications.InstalledApplication',
        related_name='certificate',
        verbose_name='Applications',
        blank = True
    ) 
    
    class Meta:
        verbose_name_plural = "Cars"
        verbose_name = 'Car'

    def get_absolute_url(self):
        return reverse('plugins:netbox_cars:cars', args=[self.pk])

    def get_status_color(self):
        return CarsStatusChoices.colors.get(self.status)
    
    def __str__(self):
        return self.name 