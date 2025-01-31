from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from adestis_netbox_certificate_management.models import *
from adestis_netbox_certificate_management.views import *
from django.urls import include
from utilities.urls import get_model_urls

urlpatterns = (
    # Certificates
    path('certificates/', CertificateListView.as_view(),
         name='certificate_list'),
    path('certificates/add/', CertificateEditView.as_view(),
         name='certificate_add'),
    path('certificates/delete/', CertificateBulkDeleteView.as_view(),
         name='certificate_bulk_delete'),
    path('certificates/edit/', CertificateBulkEditView.as_view(),
         name='certificate_bulk_edit'),
    path('certificates/import/', CertificateBulkImportView.as_view(),
         name='certificate_import'),
    path('certificates/<int:pk>/',
         CertificateView.as_view(), name='certificate'),
    path('certificates/<int:pk>/',
         include(get_model_urls("adestis_netbox_certificate_management", "certificate"))),
    path('certificates/<int:pk>/edit/',
         CertificateEditView.as_view(), name='certificate_edit'),
    path('certificates/<int:pk>/delete/',
         CertificateDeleteView.as_view(), name='certificate_delete'),
    path('certificates/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='certificate_changelog', kwargs={
        'model': Certificate
    }),

)
