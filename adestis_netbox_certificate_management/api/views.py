from adestis_netbox_certificate_management.models import Certificate
from adestis_netbox_certificate_management.filtersets.certificate import CertificateFilterSet
from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import CertificateSerializer

class CertificateViewSet(NetBoxModelViewSet):
    queryset = Certificate.objects.prefetch_related(
        'tags'
    )
    serializer_class = CertificateSerializer
    filterset_class = CertificateFilterSet