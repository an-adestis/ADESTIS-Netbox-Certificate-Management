from netbox.views import generic
from netbox_cars.forms import *
from netbox_cars.models import *
from netbox_cars.filtersets import *
from netbox_cars.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _

__all__ = (
    'CarsView',
    'CarsListView',
    'CarsEditView',
    'CarsDeleteView',
    'CarsBulkDeleteView',
    'CarsBulkEditView',
    'CarsBulkImportView',
)

class CarsView(generic.ObjectView):
    queryset = Cars.objects.all()

class CarsListView(generic.ObjectListView):
    queryset = Cars.objects.all()
    table = CarsTable
    filterset = CarsFilterSet
    filterset_form = CarsFilterForm
    

class CarsEditView(generic.ObjectEditView):
    queryset = Cars.objects.all()
    form = CarsForm


class CarsDeleteView(generic.ObjectDeleteView):
    queryset = Cars.objects.all() 

class CarsBulkDeleteView(generic.BulkDeleteView):
    queryset = Cars.objects.all()
    table = CarsTable
    
    
class CarsBulkEditView(generic.BulkEditView):
    queryset = Cars.objects.all()
    filterset = CarsFilterSet
    table = CarsTable
    form =  CarsBulkEditForm
    

class CarsBulkImportView(generic.BulkImportView):
    queryset = Cars.objects.all()
    model_form = CarsCSVForm
    table = CarsTable
    