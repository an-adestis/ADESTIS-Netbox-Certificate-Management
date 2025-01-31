from adestis_netbox_certificate_management.models import Certificate
from netbox.filtersets import NetBoxModelFilterSet
from django.db.models import Q
from django.utils.translation import gettext as _

__all__ = (
    'CertificateFilterSet',
)

class CertificateFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = Certificate
        fields = ['id', 'status']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter( Q(status__icontains=value) )
