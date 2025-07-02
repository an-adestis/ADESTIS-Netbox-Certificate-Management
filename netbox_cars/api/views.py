from netbox_cars.models import Cars
from netbox_cars.filtersets import *
from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import CarsSerializer

class CarsViewSet(NetBoxModelViewSet):
    queryset = Cars.objects.prefetch_related(
        'tags'
    )
    serializer_class = CarsSerializer
    filterset_class = CarsFilterSet