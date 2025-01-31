from netbox.views import generic
from adestis_netbox_certificate_management.forms import *
from adestis_netbox_certificate_management.models import *
from adestis_netbox_certificate_management.filtersets import *
from adestis_netbox_certificate_management.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _

__all__ = (
    'CertificateView',
    'CertificateListView',
    'CertificateEditView',
    'CertificateDeleteView',
    'CertificateBulkDeleteView',
    'CertificateBulkEditView',
    'CertificateBulkImportView',
)

class CertificateView(generic.ObjectView):
    queryset = Certificate.objects.all()


class CertificateListView(generic.ObjectListView):
    queryset = Certificate.objects.all()
    table = CertificateTable
    filterset = CertificateFilterSet
    filterset_form = CertificateFilterForm

class CertificateEditView(generic.ObjectEditView):
    queryset = Certificate.objects.all()
    form = CertificateForm


class CertificateDeleteView(generic.ObjectDeleteView):
    queryset = Certificate.objects.all()
 

class CertificateBulkDeleteView(generic.BulkDeleteView):
    queryset = Certificate.objects.all()
    table = CertificateTable
    
    
class CertificateBulkEditView(generic.BulkEditView):
    queryset = Certificate.objects.all()
    filterset = CertificateFilterSet
    table = CertificateTable
    form =  CertificateBulkEditForm
    

class CertificateBulkImportView(generic.BulkImportView):
    queryset = Certificate.objects.all()
    model_form = CertificateCSVForm
    table = CertificateTable
