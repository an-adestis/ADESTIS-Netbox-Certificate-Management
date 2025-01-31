from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *

__all__ = (
    'CertificateStatusChoices',
    'Certificate',
)

class CertificateStatusChoices(ChoiceSet):
    key = 'Certificates.status'

    STATUS_ACTIVE = 'active'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
    ]


class Certificate(NetBoxModel):

    status = models.CharField(
        max_length=50,
        choices=CertificateStatusChoices,
        verbose_name='Status',
        help_text='Status'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = "Certificates"
        verbose_name = 'Certificate'

    def __str__(self):
        # return self.logon_name
        return "Placeholder for Certificate"

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_certificate_management:certificate', args=[self.pk])

    def get_status_color(self):
        return CertificateStatusChoices.colors.get(self.status)
