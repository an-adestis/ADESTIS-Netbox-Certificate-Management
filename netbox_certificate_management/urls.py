from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from netbox_certificate_management.models import *
from netbox_certificate_management.views import *
from netbox_certificate_management.views.certificate import *
from netbox_certificate_management.models import *
from django.urls import include
from utilities.urls import get_model_urls

urlpatterns = (

    # Certificates
    path('certificate/', CertificateListView.as_view(),
         name='certificate_list'),
    path('certificate/add/', CertificateEditView.as_view(),
         name='certificate_add'),
    path('certificate/delete/', CertificateBulkDeleteView.as_view(),
         name='certificate_bulk_delete'),
    path('certificate/edit/', CertificateBulkEditView.as_view(),
         name='certificate_bulk_edit'),
    path('certificate/import/', CertificateBulkImportView.as_view(),
         name='certificate_bulk_import'),
    path('certificates/import_certificate/', CertificateBulkImportCertificateView.as_view(), name='certificate_bulk_import_certificate'),
    
    path('certificates/applications/', CertificateAffectedInstalledApplicationView.as_view(),
         name='certificateapplications_list'),
    path('certificate/<int:pk>/',
         CertificateView.as_view(), name='certificate'),
    path('certificate/<int:pk>/',
         include(get_model_urls("netbox_certificate_management", "certificate"))),
    path('certificate/<int:pk>/edit/',
         CertificateEditView.as_view(), name='certificate_edit'),
    path('certificate/<int:pk>/delete/',
         CertificateDeleteView.as_view(), name='certificate_delete'),
    path('certificate/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='certificate_changelog', kwargs={
        'model': Certificate
    }),

)
