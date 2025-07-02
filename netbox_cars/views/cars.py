from netbox.views import generic
from netbox_cars.forms import *
from netbox_cars.models import *
from netbox_cars.filtersets import *
from netbox_cars.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from netbox_cars.models import *
from netbox_cars.tables import *
from adestis_netbox_applications.models import InstalledApplication
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view


__all__ = (
    'CarsView',
    'CarsListView',
    'CarsEditView',
    'CarsDeleteView',
    'CarsBulkDeleteView',
    'CarsBulkEditView',
    'CarsBulkImportView',
    'InstalledApplicationAffectedCarsView',
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
    
@register_model_view(InstalledApplication, name='cars')
class InstalledApplicationAffectedCarsView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= Cars
    table = CarsTable
    template_name = "netbox_cars/cars_application.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_cars': {'change'},
    }

    tab = ViewTab(
        label=_('Cars'),
        # badge=lambda obj: obj.cars.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return Cars.objects.restrict(request.user, 'view').filter(installedapplication=parent)

    